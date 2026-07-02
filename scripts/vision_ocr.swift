import AppKit
import Foundation
import Vision

struct OCRLine: Codable {
    let page: Int
    let text: String
    let confidence: Float
    let x: Double
    let y: Double
    let width: Double
    let height: Double
}

func pageNumber(from path: String, fallback: Int) -> Int {
    let name = URL(fileURLWithPath: path).deletingPathExtension().lastPathComponent
    let digits = name.reversed().prefix { $0.isNumber }.reversed()
    if let number = Int(String(digits)) {
        return number
    }
    return fallback
}

func recognize(path: String, page: Int) throws -> [OCRLine] {
    let url = URL(fileURLWithPath: path)
    guard let image = NSImage(contentsOf: url),
          let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        throw NSError(domain: "VisionOCR", code: 1, userInfo: [NSLocalizedDescriptionKey: "Unable to load image: \(path)"])
    }

    var lines: [OCRLine] = []
    let request = VNRecognizeTextRequest { request, error in
        if let error = error {
            fputs("OCR error on page \(page): \(error)\n", stderr)
            return
        }

        let observations = request.results as? [VNRecognizedTextObservation] ?? []
        for observation in observations {
            guard let candidate = observation.topCandidates(1).first else { continue }
            let box = observation.boundingBox
            lines.append(
                OCRLine(
                    page: page,
                    text: candidate.string,
                    confidence: candidate.confidence,
                    x: box.origin.x,
                    y: box.origin.y,
                    width: box.width,
                    height: box.height
                )
            )
        }
    }

    request.recognitionLevel = .accurate
    request.recognitionLanguages = ["zh-Hans", "en-US"]
    request.usesLanguageCorrection = true

    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    try handler.perform([request])
    return lines
}

let args = Array(CommandLine.arguments.dropFirst())
guard !args.isEmpty else {
    fputs("Usage: swift scripts/vision_ocr.swift PAGE_IMAGE...\n", stderr)
    exit(2)
}

var allLines: [OCRLine] = []
for (index, path) in args.enumerated() {
    let page = pageNumber(from: path, fallback: index + 1)
    fputs("OCR page \(page): \(path)\n", stderr)
    allLines.append(contentsOf: try recognize(path: path, page: page))
}

let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
let data = try encoder.encode(allLines)
FileHandle.standardOutput.write(data)
