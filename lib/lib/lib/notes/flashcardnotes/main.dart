import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:notes/screens/constants.dart';
import 'package:notes/screens/flashcardnotes/sub.dart';
import 'package:notes/screens/logo.dart';
import 'package:notes/screens/topbar.dart';

// 1. DATA MODELS: These are still useful for correctly parsing the initial JSON data.

class FlashcardImage {
  final int id;
  final String imageUrl;
  final String caption;

  FlashcardImage({
    required this.id,
    required this.imageUrl,
    required this.caption,
  });

  factory FlashcardImage.fromJson(Map<String, dynamic> json) {
    return FlashcardImage(
      id: json['id'] ?? 0,
      imageUrl: json['image'] ?? '',
      caption: json['caption'] ?? '',
    );
  }
}

class FlashcardSet {
  final int id;
  final String subjectName;
  final String description;
  final List<FlashcardImage> images;

  FlashcardSet({
    required this.id,
    required this.subjectName,
    required this.description,
    required this.images,
  });

  factory FlashcardSet.fromJson(Map<String, dynamic> json) {
    var imagesFromJson = json['images'] as List? ?? [];
    List<FlashcardImage> imageList = imagesFromJson
        .map((img) => FlashcardImage.fromJson(img))
        .toList();

    return FlashcardSet(
      id: json['id'] ?? 0,
      subjectName: json['subject_name'] ?? 'No Subject',
      description: json['description'] ?? '',
      images: imageList,
    );
  }
}

// 2. MAIN WIDGET: Fetches data and displays the count for each subject.

class FlashcardsScreen extends StatefulWidget {
  const FlashcardsScreen({super.key});

  @override
  State<FlashcardsScreen> createState() => _FlashcardsScreenState();
}

class _FlashcardsScreenState extends State<FlashcardsScreen> {
  bool _isLoading = true;
  String _errorMessage = '';
  // This new map will store the counts, e.g., {"Anatomy": 1, "Human Anatomy": 1}
  Map<String, int> _subjectCounts = {};

  @override
  void initState() {
    super.initState();
    _fetchAndProcessFlashcards();
  }

  Future<void> _fetchAndProcessFlashcards() async {
    try {
      final url = Uri.parse("${API}flashcards/");
      final response = await http.get(url).timeout(const Duration(seconds: 15));

      if (!mounted) return;

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        final List<FlashcardSet> sets = data
            .map((json) => FlashcardSet.fromJson(json))
            .toList();

        // ✅ CORE LOGIC: Group by subject_name and count the items.
        final Map<String, int> subjectCounts = {};
        for (var flashcardSet in sets) {
          subjectCounts[flashcardSet.subjectName] =
              (subjectCounts[flashcardSet.subjectName] ?? 0) + 1;
        }

        print(subjectCounts);

        setState(() {
          _subjectCounts = subjectCounts;
          _isLoading = false;
        });
      } else {
        setState(() {
          _errorMessage = "Failed to load data (Code: ${response.statusCode})";
          _isLoading = false;
        });
      }
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _errorMessage = "An error occurred: $e";
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomLogoAppBar(),
      // Updated Scaffold background color
      backgroundColor: const Color(0xFFF5F5F5), // Light grey background
      body: _buildBody(),
    );
  }

  // In _FlashcardsScreenState

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_errorMessage.isNotEmpty) {
      return Center(
        child: Text(_errorMessage, style: const TextStyle(color: Colors.red)),
      );
    }

    final subjectEntries = _subjectCounts.entries.toList();

    return Column(
      children: [
        Topbar(firstText: "Flash Card", secondText: "Subjects"),
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.all(12.0),
            itemCount: subjectEntries.length,
            itemBuilder: (context, index) {
              final entry = subjectEntries[index];
              final subjectName = entry.key;
              final count = entry.value;

              return Padding(
                padding: const EdgeInsets.only(bottom: 12.0),
                child: InkWell(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute<void>(
                        builder: (context) =>
                            FlashcardDetailScreen(subjectName: subjectName),
                      ),
                    );
                  },
                  child: Card(
                    elevation: 1,
                    color: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                    margin: EdgeInsets.zero,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Padding(
                          padding: const EdgeInsets.fromLTRB(16, 16, 16, 20),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                subjectName,
                                style: const TextStyle(
                                  fontWeight: FontWeight.w600,
                                  fontSize: 20,
                                  color: Colors.black87,
                                ),
                              ),
                              Text(
                                '$count ${count == 1 ? "Card" : "Cards"}',
                                style: TextStyle(
                                  fontWeight: FontWeight.w400,
                                  fontSize: 20,
                                  color: Colors.black,
                                ),
                              ),
                            ],
                          ),
                        ),
                        Container(
                          height: 15,
                          decoration: const BoxDecoration(
                            color: Color(0xFF00897B),
                            borderRadius: BorderRadius.only(
                              bottomLeft: Radius.circular(8),
                              bottomRight: Radius.circular(8),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}
