import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:notes/screens/constants.dart';
import 'package:notes/screens/logo.dart';

class ClinicalCaseDetailScreen extends StatefulWidget {
  final String caseTitle;
  const ClinicalCaseDetailScreen({super.key, required this.caseTitle});

  @override
  State<ClinicalCaseDetailScreen> createState() =>
      _ClinicalCaseDetailScreenState();
}

class _ClinicalCaseDetailScreenState extends State<ClinicalCaseDetailScreen> {
  bool _isLoading = true;
  String _errorMessage = '';
  Map<String, dynamic>? _caseData;
  int _expandedPanelIndex = -1;

  @override
  void initState() {
    super.initState();
    _fetchCaseByTitle();
  }

  Future<void> _fetchCaseByTitle() async {
    try {
      final url = Uri.parse("${API}clinical-cases/");
      final response = await http.get(url).timeout(const Duration(seconds: 15));

      if (!mounted) return;

      if (response.statusCode == 200) {
        final List data = jsonDecode(response.body);
        final matchingCase = data.firstWhere(
          (item) => item['case_title'] == widget.caseTitle,
          orElse: () => null,
        );

        if (matchingCase != null) {
          setState(() {
            _caseData = matchingCase;
            _isLoading = false;
          });
        } else {
          setState(() {
            _errorMessage = "Case not found.";
            _isLoading = false;
          });
        }
      } else {
        setState(() {
          _errorMessage = "Failed to load cases (Code: ${response.statusCode})";
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

  void _onExpansionChanged(bool isExpanded, int index) {
    setState(() {
      _expandedPanelIndex = isExpanded ? index : -1;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(color: Color(0xFF1B5E20)),
        ),
      );
    }
    if (_errorMessage.isNotEmpty) {
      return Scaffold(
        body: Center(
          child: Text(
            _errorMessage,
            style: const TextStyle(color: Color(0xFFD32F2F)),
          ),
        ),
      );
    }

    final String caseTitle = _caseData!['case_title'] as String;
    final String doctorName = _caseData!['doctor_name'] as String;

    final List<Map<String, String>> sections = [
      {
        'title': 'Gather Equipments',
        'content': _caseData!['gather_equipments'].toString(),
      },
      {
        'title': 'Introduction',
        'content': _caseData!['introduction'].toString(),
      },
      {
        'title': 'General Inspection',
        'content': _caseData!['general_inspection'].toString(),
      },
      {
        'title': 'Closer Inspection',
        'content': _caseData!['closer_inspection'].toString(),
      },
      {'title': 'Palpation', 'content': _caseData!['palpation'].toString()},
      {
        'title': 'Final Examination',
        'content': _caseData!['final_examination'].toString(),
      },
      {'title': 'References', 'content': _caseData!['references'].toString()},
    ];

    return Scaffold(
      appBar: CustomLogoAppBar(),
      backgroundColor: Colors.white,
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            backgroundColor: const Color(0xFF1B5E20),
            expandedHeight: 250.0,
            floating: false,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              background: Stack(
                fit: StackFit.expand,
                children: [
                  // This is where your image goes.
                  // For example, replace this with:
                  Image.asset('assets/over.png', fit: BoxFit.cover),

                  Positioned.fill(
                    child: Align(
                      alignment: Alignment.center,
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            caseTitle, // Use the dynamic title
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            doctorName, // Use the dynamic doctor's name
                            style: TextStyle(
                              color: Colors.white.withOpacity(0.8),
                              fontSize: 16,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          SliverList(
            delegate: SliverChildBuilderDelegate((context, index) {
              if (index == 0) {
                return _buildTableOfContents(sections);
              }

              final section = sections[index - 1];
              return _buildExpansionTile(
                title: section['title']!,
                content: section['content']!,
                index: index,
                isExpanded: _expandedPanelIndex == index,
              );
            }, childCount: sections.length + 1),
          ),
        ],
      ),
    );
  }

  Widget _buildTableOfContents(List<Map<String, String>> sections) {
    return Column(
      children: [
        const Divider(color: Color(0xFFEEEEEE), height: 1),
        ExpansionTile(
          initiallyExpanded: _expandedPanelIndex == 0,
          onExpansionChanged: (expanded) => _onExpansionChanged(expanded, 0),
          tilePadding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
          title: const Text(
            'Table of contents',
            style: TextStyle(
              color: Color(0xFF037E73),
              fontWeight: FontWeight.w600,
              fontSize: 25,
            ),
          ),
          trailing: Icon(
            _expandedPanelIndex == 0
                ? Icons.keyboard_arrow_up
                : Icons.keyboard_arrow_down,
            color: const Color(0xFF037E73),
            size: 25,
          ),
          children: sections
              .asMap()
              .entries
              .map(
                (entry) => Padding(
                  padding: const EdgeInsets.only(left: 32.0, right: 16.0),
                  child: ListTile(
                    title: Text(
                      '${entry.key + 1}. ${entry.value['title']}',
                      style: const TextStyle(
                        color: Color(0xFF037E73),
                        fontWeight: FontWeight.w400,
                        fontSize: 22,
                        decoration: TextDecoration.underline,
                      ),
                    ),
                    onTap: () {
                      _onExpansionChanged(true, entry.key + 1);
                    },
                  ),
                ),
              )
              .toList(),
        ),
      ],
    );
  }

  Widget _buildExpansionTile({
    required String title,
    required String content,
    required int index,
    required bool isExpanded,
  }) {
    return Column(
      children: [
        const Divider(color: Color(0xFFEEEEEE), height: 1),
        ExpansionTile(
          initiallyExpanded: isExpanded,
          onExpansionChanged: (expanded) =>
              _onExpansionChanged(expanded, index),
          tilePadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          title: Text(
            title,
            style: const TextStyle(
              color: Color(0xFF037E73),
              fontWeight: FontWeight.w600,
              fontSize: 22,
            ),
          ),
          trailing: Icon(
            isExpanded ? Icons.keyboard_arrow_up : Icons.keyboard_arrow_down,
            color: const Color(0xFF037E73),
          ),
          children: [
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Text(
                content,
                style: const TextStyle(fontSize: 22, height: 1.5),
              ),
            ),
          ],
        ),
      ],
    );
  }
}
