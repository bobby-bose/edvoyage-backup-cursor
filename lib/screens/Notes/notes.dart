import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/screens/notes/constants.dart';
import 'package:frontend/screens/notes/logo.dart';
import 'package:frontend/screens/notes/main.dart';
import 'package:frontend/screens/notes/topbar.dart';
import 'package:frontend/screens/notes/videonotes/sub.dart'; // VideoTopicsScreen
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import 'package:frontend/main.dart';

// Data model for a Category
class Category {
  final int id;
  final String name;

  Category({required this.id, required this.name});

  factory Category.fromJson(Map<String, dynamic> json) {
    return Category(id: json['id'], name: json['name']);
  }
}

class VideoSubjectScreen extends StatefulWidget {
  const VideoSubjectScreen({super.key});

  @override
  State<VideoSubjectScreen> createState() => _VideoSubjectScreenState();
}

class _VideoSubjectScreenState extends State<VideoSubjectScreen> {
  Measurements? size;
  bool isLoading = true;
  List<Category> categories = []; // Correct type: List<Category>

  @override
  void initState() {
    super.initState();
    fetchCategories();
  }

  Future<void> fetchCategories() async {
    try {
      final response = await http.get(Uri.parse("${API}categories/"));

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);

        final List<Category> tempCategories =
            data.map((json) => Category.fromJson(json)).toList();

        setState(() {
          categories = tempCategories;
          isLoading = false;
        });
      } else {
        throw Exception('Failed to load categories');
      }
    } catch (e) {
      setState(() {
        isLoading = false;
      });
      debugPrint("Error fetching categories: $e");
    }
  }

  Widget buildCategoryCard(Category category) {
    return GestureDetector(
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => NotesScreen(className: category.name),
          ),
        );
      },
      child: Card(
        elevation: 2,
        clipBehavior: Clip.antiAlias,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16.0),
        ),
        margin: const EdgeInsets.symmetric(vertical: 10, horizontal: 16),
        child: SizedBox(
          height: 200,
          width: double.infinity,
          child: Column(
            children: [
              ListTile(
                title: Text(
                  category.name,
                  style: const TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                trailing: const Icon(Icons.more_vert),
              ),
              const Expanded(child: SizedBox()),
              const SizedBox(height: 16),
              Container(
                height: 20,
                width: double.infinity,
                color: primaryColor,
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);

    return Scaffold(
      appBar: CustomLogoAppBar(),
      body: Column(
        children: [
          Topbar(firstText: "Edvoyage", secondText: "Notes"),
          Expanded(
            child: isLoading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    padding: const EdgeInsets.only(top: 10),
                    itemCount: categories.length,
                    itemBuilder: (context, index) {
                      return buildCategoryCard(categories[index]);
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
