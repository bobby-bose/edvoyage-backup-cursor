import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:notes/screens/clinicalnotes/sub.dart';
import 'package:notes/screens/constants.dart';
import 'package:notes/screens/logo.dart';

// 1. DATA MODEL: Represents a single clinical case from the API
class ClinicalCase {
  final int id;
  final String caseTitle;
  final String doctorName;
  // subjectName is no longer in the API response but we keep the model flexible
  // by giving it a default value in fromJson.
  final String subjectName;
  final String gatherEquipments;
  final String introduction;
  final String generalInspection;
  final String closerInspection;
  final String palpation;
  final String finalExamination;
  final String? references;
  final DateTime createdAt;

  ClinicalCase({
    required this.id,
    required this.caseTitle,
    required this.doctorName,
    required this.subjectName,
    required this.gatherEquipments,
    required this.introduction,
    required this.generalInspection,
    required this.closerInspection,
    required this.palpation,
    required this.finalExamination,
    this.references,
    required this.createdAt,
  });

  factory ClinicalCase.fromJson(Map<String, dynamic> json) {
    return ClinicalCase(
      id: json['id'] ?? 0,
      caseTitle: json['case_title'] ?? 'No Title',
      doctorName: json['doctor_name'] ?? 'N/A',
      subjectName:
          json['subject_name'] ?? 'N/A', // Handles missing field gracefully
      gatherEquipments: json['gather_equipments'] ?? '',
      introduction: json['introduction'] ?? '',
      generalInspection: json['general_inspection'] ?? '',
      closerInspection: json['closer_inspection'] ?? '',
      palpation: json['palpation'] ?? '',
      finalExamination: json['final_examination'] ?? '',
      references: json['references'],
      createdAt: DateTime.tryParse(json['created_at'] ?? '') ?? DateTime.now(),
    );
  }
}

// 2. MAIN WIDGET: The screen that fetches and displays the data
class ClinicalCasesScreen extends StatefulWidget {
  const ClinicalCasesScreen({super.key});

  @override
  State<ClinicalCasesScreen> createState() => _ClinicalCasesScreenState();
}

class _ClinicalCasesScreenState extends State<ClinicalCasesScreen> {
  bool _isLoading = true;
  String _errorMessage = '';
  List<ClinicalCase> _cases = [];
  // The subjectCounts map is no longer needed

  @override
  void initState() {
    super.initState();
    _fetchClinicalCases();
  }

  Future<void> _fetchClinicalCases() async {
    try {
      final url = Uri.parse("${API}clinical-cases/");
      final response = await http.get(url).timeout(const Duration(seconds: 15));

      if (!mounted) return;

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        final List<ClinicalCase> cases = data
            .map((json) => ClinicalCase.fromJson(json))
            .toList();

        // The subject counting logic is no longer needed.

        setState(() {
          _cases = cases;
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
      // ✅ MODIFIED: AppBar title updated
      appBar: CustomLogoAppBar(),
      backgroundColor: Colors.grey[200],
      body: _buildBody(),
    );
  }

  // In clinical_cases_screen.dart

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_errorMessage.isNotEmpty) {
      return Center(
        child: Text(
          _errorMessage,
          style: const TextStyle(color: Colors.red, fontSize: 16),
        ),
      );
    }

    return ListView.builder(
      itemCount: _cases.length,
      padding: const EdgeInsets.all(8.0),
      itemBuilder: (context, index) {
        final clinicalCase = _cases[index];
        return InkWell(
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) =>
                    ClinicalCaseDetailScreen(caseTitle: clinicalCase.caseTitle),
              ),
            );
          },
          child: Card(
            margin: const EdgeInsets.symmetric(
              vertical: 25.0,
              horizontal: 15.0,
            ),
            elevation: 2,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(15),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 12, 16, 25),
                  child: Text(
                    clinicalCase.caseTitle,
                    style: const TextStyle(
                      fontSize: 25,
                      fontWeight: FontWeight.bold,
                      color: Colors.black87,
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      Text(
                        clinicalCase.doctorName,
                        style: TextStyle(fontSize: 20, color: Colors.grey[700]),
                      ),
                    ],
                  ),
                ),
                // ✅ Green bottom border
                Container(
                  height: 15,
                  decoration: BoxDecoration(
                    color: Colors.teal, // green border
                    borderRadius: const BorderRadius.only(
                      bottomLeft: Radius.circular(8),
                      bottomRight: Radius.circular(8),
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
