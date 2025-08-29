import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:frontend/screens/Notes/clinicalnotes/main.dart';
import 'package:frontend/screens/Notes/flashcardnotes/main.dart';
import 'package:frontend/screens/Notes/mcqnotes/main.dart';
import 'package:frontend/screens/Notes/questionbanknotes/main.dart';
import 'package:frontend/screens/Notes/videonotes/main.dart';
import 'package:frontend/screens/notification/notification.dart';
import 'package:frontend/utils/avatar.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import 'package:frontend/widgets/botttom_nav.dart';
import 'package:http/http.dart' as http;

class NotesSection extends StatefulWidget {
  const NotesSection({super.key});

  @override
  State<NotesSection> createState() => _NotesDashboardPageState();
}

class _NotesDashboardPageState extends State<NotesSection> {
  Measurements? size;
  bool isLoading = true;
  Map<String, dynamic> counts = {
    'video': {'topics': 0, 'videos': 0},
    'mcq': {'topics': 0, 'modules': 0},
    'clinical_case': {'topics': 0, 'modules': 0},
    'q_bank': {'topics': 0, 'modules': 0},
    'flash_card': {'topics': 0, 'modules': 0},
  };

  @override
  void initState() {
    super.initState();
    fetchCounts();
  }

  Future<void> fetchCounts() async {
    try {
      final responses = await Future.wait([
        http.get(Uri.parse("http://localhost:8000/api/v1/notes/notesvideos/")),
        http.get(Uri.parse("http://localhost:8000/api/v1/notes/notesmcqs/")),
        http.get(Uri.parse(
            "http://localhost:8000/api/v1/notes/notesclinicalcases/")),
        http.get(Uri.parse("http://localhost:8000/api/v1/notes/notesqbank/")),
        http.get(
            Uri.parse("http://localhost:8000/api/v1/notes/notesflashcards/")),
      ]);

      setState(() {
        counts['video']['videos'] = jsonDecode(responses[0].body).length;
        counts['mcq']['modules'] = jsonDecode(responses[1].body).length;
        counts['clinical_case']['modules'] =
            jsonDecode(responses[2].body).length;
        counts['q_bank']['modules'] = jsonDecode(responses[3].body).length;
        counts['flash_card']['modules'] = jsonDecode(responses[4].body).length;
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        isLoading = false;
      });
      debugPrint("Error fetching counts: $e");
    }
  }

  Widget buildCard(String title, String key, String subKey, String label,
      Widget navigateTo) {
    final countValue = counts[key]?[subKey]?.toString() ?? "0";

    return GestureDetector(
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => navigateTo),
        );
      },
      child: Card(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
        elevation: 5,
        margin: const EdgeInsets.symmetric(vertical: 15, horizontal: 25),
        child: ListTile(
          contentPadding:
              const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
          title: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style:
                    const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 3),
              isLoading
                  ? const Text("Loading...")
                  : Text(
                      "$countValue $label",
                      style:
                          const TextStyle(fontSize: 14, color: Colors.black87),
                    ),
            ],
          ),
          trailing: const Icon(Icons.arrow_forward_ios, color: Colors.teal),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return Scaffold(
      bottomNavigationBar: BottomButton(onTap: () {}, selectedIndex: 3),
      appBar: AppBar(
        leading: IconButton(
          icon: Icon(
            Icons.arrow_back_ios_new,
            color: primaryColor,
            size: size!.hp(3.5), // Slightly larger than default
            weight: 700, // For a little thickness (Flutter 3.7+)
          ),
          onPressed: () {
            Navigator.of(context).pop();
          },
        ),
        backgroundColor: Colors.white,
        elevation: 0.2,
        automaticallyImplyLeading: false,
        centerTitle: true,
        title: SizedBox(
          height: 250, // Set the width of the container
          width: 200, // Set the height of the container
          child:
              Image.asset(edvoyagelogo1), // Replace with the actual image path
        ),
        actions: [
          IconButton(
              icon: Icon(
                Icons.notifications,
                color: primaryColor,
              ),
              onPressed: () {
                Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (context) => NotificationScreen()));
              })
        ],
      ),
      body: ListView(
        children: [
          buildCard("Videos", "video", "videos", "Videos", VideoNotesScreen()),
          buildCard("MCQs", "mcq", "modules", "MCQs", MCQNotesScreen()),
          buildCard("Clinical Cases", "clinical_case", "modules",
              "Clinical Cases", ClinicalCasesScreen()),
          buildCard("Q Bank", "q_bank", "modules", "Q Bank", QBankScreen()),
          buildCard("Flash Cards", "flash_card", "modules", "Flash Cards",
              FlashCardModulesScreen()),
        ],
      ),
    );
  }
}
