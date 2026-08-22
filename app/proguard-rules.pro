# WebView + JS arayüzü korunur
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
