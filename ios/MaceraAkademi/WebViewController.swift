import AVFoundation
import UIKit
import UniformTypeIdentifiers
import WebKit

final class WebViewController: UIViewController {
    private enum Constants {
        static let scheme = "macera"
        static let host = "app"
        static let startPage = "macera-akademi.html"
        static let messageHandler = "tts"
        static let background = UIColor(red: 36 / 255, green: 26 / 255, blue: 61 / 255, alpha: 1)
    }

    private let speechSynthesizer = AVSpeechSynthesizer()
    private let turkishVoice = WebViewController.bestTurkishVoice()
    private let schemeHandler = BundleSchemeHandler()
    private var webView: WKWebView!
    private var splashView: UIView?
    private var splashFallback: DispatchWorkItem?

    override func viewDidLoad() {
        super.viewDidLoad()

#if DEBUG
        print("[MaceraTTS] Türkçe ses: \(turkishVoice?.identifier ?? "bulunamadı")")
#endif

        view.backgroundColor = Constants.background
        configureWebView()
        installSplash()
        loadStartPage()

        NotificationCenter.default.addObserver(
            self,
            selector: #selector(stopSpeech),
            name: UIApplication.willResignActiveNotification,
            object: nil
        )
    }

    deinit {
        splashFallback?.cancel()
        NotificationCenter.default.removeObserver(self)
        webView?.configuration.userContentController.removeScriptMessageHandler(forName: Constants.messageHandler)
    }

    override var preferredStatusBarStyle: UIStatusBarStyle { .lightContent }
    override var supportedInterfaceOrientations: UIInterfaceOrientationMask { .portrait }
    override var shouldAutorotate: Bool { false }

    private func configureWebView() {
        let contentController = WKUserContentController()
        contentController.add(self, name: Constants.messageHandler)
        contentController.addUserScript(
            WKUserScript(
                source: Self.nativeSpeechBridge(
                    voiceAvailable: turkishVoice != nil,
                    voiceName: turkishVoice?.name ?? ""
                ),
                injectionTime: .atDocumentStart,
                forMainFrameOnly: false
            )
        )

        let configuration = WKWebViewConfiguration()
        configuration.userContentController = contentController
        configuration.websiteDataStore = .default()
        configuration.allowsInlineMediaPlayback = true
        configuration.mediaTypesRequiringUserActionForPlayback = []
        configuration.defaultWebpagePreferences.allowsContentJavaScript = true
        configuration.setURLSchemeHandler(schemeHandler, forURLScheme: Constants.scheme)

        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.translatesAutoresizingMaskIntoConstraints = false
        webView.navigationDelegate = self
        webView.uiDelegate = self
        webView.isOpaque = false
        webView.backgroundColor = Constants.background
        webView.scrollView.backgroundColor = Constants.background
        webView.scrollView.bounces = false
        webView.scrollView.alwaysBounceVertical = false
        webView.scrollView.alwaysBounceHorizontal = false
        webView.scrollView.keyboardDismissMode = .interactive
        webView.allowsBackForwardNavigationGestures = false

#if DEBUG
        if #available(iOS 16.4, *) {
            webView.isInspectable = true
        }
#endif

        view.addSubview(webView)
        NSLayoutConstraint.activate([
            webView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            webView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            webView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            webView.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor)
        ])

        self.webView = webView
    }

    private func loadStartPage() {
        guard let resourceRoot = Bundle.main.resourceURL,
              let url = Bundle.main.url(forResource: "macera-akademi", withExtension: "html") else {
            showLoadError("Başlangıç dosyası bulunamadı.")
            return
        }
        webView.loadFileURL(url, allowingReadAccessTo: resourceRoot)
    }

    // The catalog is a single 1.7 MB HTML document; WKWebView needs several
    // seconds to parse it. Without this layer the app shows a bare background
    // for that whole time and looks stalled on first launch.
    private func installSplash() {
        let splash = UIView()
        splash.translatesAutoresizingMaskIntoConstraints = false
        splash.backgroundColor = Constants.background

        let title = UILabel()
        title.translatesAutoresizingMaskIntoConstraints = false
        title.text = "Macera Akademi"
        title.textColor = .white
        title.font = .systemFont(ofSize: 28, weight: .heavy)
        title.textAlignment = .center

        let subtitle = UILabel()
        subtitle.translatesAutoresizingMaskIntoConstraints = false
        subtitle.text = "Maceralar hazırlanıyor…"
        subtitle.textColor = UIColor.white.withAlphaComponent(0.75)
        subtitle.font = .systemFont(ofSize: 16, weight: .medium)
        subtitle.textAlignment = .center

        let spinner = UIActivityIndicatorView(style: .large)
        spinner.translatesAutoresizingMaskIntoConstraints = false
        spinner.color = .white
        spinner.startAnimating()

        let stack = UIStackView(arrangedSubviews: [title, spinner, subtitle])
        stack.translatesAutoresizingMaskIntoConstraints = false
        stack.axis = .vertical
        stack.alignment = .center
        stack.spacing = 20
        stack.setCustomSpacing(28, after: title)

        splash.addSubview(stack)
        view.addSubview(splash)

        NSLayoutConstraint.activate([
            splash.topAnchor.constraint(equalTo: view.topAnchor),
            splash.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            splash.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            splash.bottomAnchor.constraint(equalTo: view.bottomAnchor),
            stack.centerXAnchor.constraint(equalTo: splash.centerXAnchor),
            stack.centerYAnchor.constraint(equalTo: splash.centerYAnchor),
            stack.leadingAnchor.constraint(greaterThanOrEqualTo: splash.leadingAnchor, constant: 24),
            stack.trailingAnchor.constraint(lessThanOrEqualTo: splash.trailingAnchor, constant: -24)
        ])

        splashView = splash

        // Should a navigation callback never arrive, the layer must not trap the
        // user behind it forever.
        let fallback = DispatchWorkItem { [weak self] in self?.hideSplash() }
        splashFallback = fallback
        DispatchQueue.main.asyncAfter(deadline: .now() + 30, execute: fallback)
    }

    private func hideSplash() {
        splashFallback?.cancel()
        splashFallback = nil

        guard let splash = splashView else { return }
        splashView = nil

        UIView.animate(
            withDuration: 0.35,
            animations: { splash.alpha = 0 },
            completion: { _ in splash.removeFromSuperview() }
        )
    }

    private func speak(_ text: String) {
        let trimmed = text.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return }

        speechSynthesizer.stopSpeaking(at: .immediate)

        do {
            let session = AVAudioSession.sharedInstance()
            try session.setCategory(.playback, mode: .spokenAudio, options: [.duckOthers])
            try session.setActive(true, options: [])
        } catch {
            // AVSpeechSynthesizer still works with the current audio session on most devices.
        }

        // A Turkish voice must be selected explicitly. Letting the synthesizer
        // choose a default when the simulator has no Turkish asset installed
        // makes Turkish text sound as if it is being read by a foreign voice.
        guard let turkishVoice else { return }

        let utterance = AVSpeechUtterance(string: trimmed)
        utterance.voice = turkishVoice
        utterance.rate = 0.43
        utterance.pitchMultiplier = 1
        utterance.volume = 1
        speechSynthesizer.speak(utterance)
    }

    @objc private func stopSpeech() {
        speechSynthesizer.stopSpeaking(at: .immediate)
    }

    private static func bestTurkishVoice() -> AVSpeechSynthesisVoice? {
        let voices = AVSpeechSynthesisVoice.speechVoices().filter {
            Locale(identifier: $0.language).languageCode == "tr"
        }

        return voices.sorted { lhs, rhs in
            if lhs.quality != rhs.quality { return lhs.quality.rawValue > rhs.quality.rawValue }
            return lhs.language == "tr-TR" && rhs.language != "tr-TR"
        }.first
    }

    private func openExternally(_ url: URL) {
        guard UIApplication.shared.canOpenURL(url) else { return }
        UIApplication.shared.open(url)
    }

    private func showLoadError(_ detail: String) {
        let alert = UIAlertController(
            title: "Macera Akademi açılamadı",
            message: detail,
            preferredStyle: .alert
        )
        alert.addAction(UIAlertAction(title: "Yeniden dene", style: .default) { [weak self] _ in
            self?.installSplash()
            self?.loadStartPage()
        })
        present(alert, animated: true)
    }

    private static func nativeSpeechBridge(voiceAvailable: Bool, voiceName: String) -> String {
        let availableLiteral = voiceAvailable ? "true" : "false"
        let encodedName = (try? JSONSerialization.data(withJSONObject: voiceName, options: [.fragmentsAllowed]))
            .flatMap { String(data: $0, encoding: .utf8) } ?? "\"\""

        return #"""
    (() => {
      try {
        Object.defineProperty(window, '__NATIVE_IOS', {
          configurable: false,
          enumerable: false,
          writable: false,
          value: true
        });
      } catch (_) {
        window.__NATIVE_IOS = true;
      }

      const send = (action, text = '') => {
        try {
          window.webkit.messageHandlers.tts.postMessage({ action, text: String(text ?? '') });
          return true;
        } catch (_) {
          return false;
        }
      };

      const voiceAvailable = __VOICE_AVAILABLE__;
      const voiceName = __VOICE_NAME__;
      const bridge = Object.freeze({
        speak(text) { return voiceAvailable ? send('speak', text) : false; },
        stop() { return send('stop'); },
        status() { return voiceAvailable ? 'ok' : 'missing'; },
        voice() { return voiceAvailable ? voiceName : ''; }
      });

      try {
        Object.defineProperty(window, 'AndroidTTS', {
          configurable: true,
          enumerable: false,
          writable: false,
          value: bridge
        });
      } catch (_) {
        window.AndroidTTS = bridge;
      }
    })();
    """#
        .replacingOccurrences(of: "__VOICE_AVAILABLE__", with: availableLiteral)
        .replacingOccurrences(of: "__VOICE_NAME__", with: encodedName)
    }
}

extension WebViewController: WKScriptMessageHandler {
    func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
        guard message.name == Constants.messageHandler,
              let body = message.body as? [String: Any],
              let action = body["action"] as? String else {
            return
        }

        switch action {
        case "speak":
            speak(body["text"] as? String ?? "")
        case "stop":
            stopSpeech()
        default:
            break
        }
    }
}

extension WebViewController: WKNavigationDelegate {
    func webView(
        _ webView: WKWebView,
        decidePolicyFor navigationAction: WKNavigationAction,
        decisionHandler: @escaping (WKNavigationActionPolicy) -> Void
    ) {
        guard let url = navigationAction.request.url else {
            decisionHandler(.cancel)
            return
        }

        let scheme = url.scheme?.lowercased()
        if scheme == Constants.scheme || scheme == "file" || scheme == "about" || scheme == "data" || scheme == "blob" {
            decisionHandler(.allow)
            return
        }

        if navigationAction.targetFrame?.isMainFrame == false {
            decisionHandler(.allow)
            return
        }

        if ["https", "http", "mailto", "tel"].contains(scheme ?? "") {
            openExternally(url)
        }
        decisionHandler(.cancel)
    }

    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        hideSplash()
    }

    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        hideSplash()
        showLoadError(error.localizedDescription)
    }

    func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
        hideSplash()
        showLoadError(error.localizedDescription)
    }
}

extension WebViewController: WKUIDelegate {
    func webView(
        _ webView: WKWebView,
        createWebViewWith configuration: WKWebViewConfiguration,
        for navigationAction: WKNavigationAction,
        windowFeatures: WKWindowFeatures
    ) -> WKWebView? {
        if let url = navigationAction.request.url {
            openExternally(url)
        }
        return nil
    }

    func webView(
        _ webView: WKWebView,
        runJavaScriptAlertPanelWithMessage message: String,
        initiatedByFrame frame: WKFrameInfo,
        completionHandler: @escaping () -> Void
    ) {
        let alert = UIAlertController(title: "Macera Akademi", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "Tamam", style: .default) { _ in completionHandler() })
        present(alert, animated: true)
    }
}

private final class BundleSchemeHandler: NSObject, WKURLSchemeHandler {
    func webView(_ webView: WKWebView, start urlSchemeTask: WKURLSchemeTask) {
        guard let requestURL = urlSchemeTask.request.url,
              requestURL.host == "app",
              let resourceRoot = Bundle.main.resourceURL else {
            fail(urlSchemeTask, code: .fileNoSuchFile)
            return
        }

        let relativePath = requestURL.path.removingPercentEncoding?
            .trimmingCharacters(in: CharacterSet(charactersIn: "/")) ?? ""
        let fileURL = resourceRoot.appendingPathComponent(relativePath).standardizedFileURL
        let rootPath = resourceRoot.standardizedFileURL.path + "/"

        guard !relativePath.isEmpty,
              fileURL.path.hasPrefix(rootPath),
              FileManager.default.fileExists(atPath: fileURL.path) else {
            fail(urlSchemeTask, code: .fileNoSuchFile)
            return
        }

        do {
            let data = try Data(contentsOf: fileURL, options: .mappedIfSafe)
            let mimeType = UTType(filenameExtension: fileURL.pathExtension)?.preferredMIMEType
                ?? "application/octet-stream"
            let response = URLResponse(
                url: requestURL,
                mimeType: mimeType,
                expectedContentLength: data.count,
                textEncodingName: mimeType.hasPrefix("text/") || mimeType.contains("javascript") ? "utf-8" : nil
            )
            urlSchemeTask.didReceive(response)
            urlSchemeTask.didReceive(data)
            urlSchemeTask.didFinish()
        } catch {
            urlSchemeTask.didFailWithError(error)
        }
    }

    func webView(_ webView: WKWebView, stop urlSchemeTask: WKURLSchemeTask) {}

    private func fail(_ task: WKURLSchemeTask, code: CocoaError.Code) {
        task.didFailWithError(CocoaError(code))
    }
}
