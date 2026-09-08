import AppKit
import ImageIO
import UniformTypeIdentifiers

let outputPath = CommandLine.arguments.dropFirst().first
    ?? "ios/MaceraAkademi/Assets.xcassets/AppIcon.appiconset/AppIcon.png"
let size = 1024
let colorSpace = CGColorSpaceCreateDeviceRGB()

guard let context = CGContext(
    data: nil,
    width: size,
    height: size,
    bitsPerComponent: 8,
    bytesPerRow: size * 4,
    space: colorSpace,
    bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue
) else {
    fatalError("İkon tuvali oluşturulamadı")
}

let graphics = NSGraphicsContext(cgContext: context, flipped: false)

NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = graphics

let canvas = NSRect(x: 0, y: 0, width: size, height: size)
NSGradient(
    starting: NSColor(red: 1, green: 215 / 255, blue: 234 / 255, alpha: 1),
    ending: NSColor(red: 134 / 255, green: 220 / 255, blue: 236 / 255, alpha: 1)
)?.draw(in: canvas, angle: -90)

context.translateBy(x: 0, y: CGFloat(size))
context.scaleBy(x: CGFloat(size) / 108, y: -CGFloat(size) / 108)

func fill(_ color: NSColor, path: NSBezierPath) {
    color.setFill()
    path.fill()
}

let orangeDark = NSColor(red: 232 / 255, green: 118 / 255, blue: 58 / 255, alpha: 1)
let orange = NSColor(red: 245 / 255, green: 142 / 255, blue: 66 / 255, alpha: 1)
let brown = NSColor(red: 58 / 255, green: 42 / 255, blue: 26 / 255, alpha: 1)

let leftEar = NSBezierPath()
leftEar.move(to: NSPoint(x: 34, y: 27))
leftEar.line(to: NSPoint(x: 44, y: 52))
leftEar.line(to: NSPoint(x: 25, y: 54))
leftEar.close()
fill(orangeDark, path: leftEar)

let rightEar = NSBezierPath()
rightEar.move(to: NSPoint(x: 74, y: 27))
rightEar.line(to: NSPoint(x: 64, y: 52))
rightEar.line(to: NSPoint(x: 83, y: 54))
rightEar.close()
fill(orangeDark, path: rightEar)

let face = NSBezierPath()
face.move(to: NSPoint(x: 54, y: 39))
face.curve(to: NSPoint(x: 84, y: 65), controlPoint1: NSPoint(x: 71, y: 39), controlPoint2: NSPoint(x: 84, y: 51))
face.curve(to: NSPoint(x: 54, y: 87), controlPoint1: NSPoint(x: 84, y: 79), controlPoint2: NSPoint(x: 71, y: 87))
face.curve(to: NSPoint(x: 24, y: 65), controlPoint1: NSPoint(x: 37, y: 87), controlPoint2: NSPoint(x: 24, y: 79))
face.curve(to: NSPoint(x: 54, y: 39), controlPoint1: NSPoint(x: 24, y: 51), controlPoint2: NSPoint(x: 37, y: 39))
face.close()
fill(orange, path: face)

let muzzle = NSBezierPath()
muzzle.move(to: NSPoint(x: 54, y: 61))
muzzle.curve(to: NSPoint(x: 70, y: 74), controlPoint1: NSPoint(x: 63, y: 61), controlPoint2: NSPoint(x: 70, y: 67))
muzzle.curve(to: NSPoint(x: 54, y: 87), controlPoint1: NSPoint(x: 70, y: 81), controlPoint2: NSPoint(x: 63, y: 87))
muzzle.curve(to: NSPoint(x: 38, y: 74), controlPoint1: NSPoint(x: 45, y: 87), controlPoint2: NSPoint(x: 38, y: 81))
muzzle.curve(to: NSPoint(x: 54, y: 61), controlPoint1: NSPoint(x: 38, y: 67), controlPoint2: NSPoint(x: 45, y: 61))
muzzle.close()
fill(.white, path: muzzle)

fill(brown, path: NSBezierPath(ovalIn: NSRect(x: 39, y: 54, width: 8, height: 8)))
fill(brown, path: NSBezierPath(ovalIn: NSRect(x: 61, y: 54, width: 8, height: 8)))
fill(brown, path: NSBezierPath(ovalIn: NSRect(x: 50, y: 65.8, width: 8, height: 6.4)))

NSGraphicsContext.restoreGraphicsState()

guard let image = context.makeImage() else { fatalError("İkon görüntüsü üretilemedi") }
let outputURL = URL(fileURLWithPath: outputPath) as CFURL
guard let destination = CGImageDestinationCreateWithURL(
    outputURL,
    UTType.png.identifier as CFString,
    1,
    nil
) else {
    fatalError("PNG hedefi oluşturulamadı")
}
CGImageDestinationAddImage(destination, image, nil)
guard CGImageDestinationFinalize(destination) else { fatalError("PNG yazılamadı") }
print("App icon written to \(outputPath)")
