import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class ClinicalCaseDetailScreen extends StatefulWidget {
  final String caseTitle;
  final String doctorName;

  const ClinicalCaseDetailScreen({
    super.key,
    required this.caseTitle,
    required this.doctorName,
  });

  @override
  _ClinicalCaseDetailScreenState createState() =>
      _ClinicalCaseDetailScreenState();
}

class _ClinicalCaseDetailScreenState extends State<ClinicalCaseDetailScreen> {
  late Future<Map<String, dynamic>> caseDataFuture;
  int _selectedIndex = 3; // Notes tab is active
  int _expandedIndex = -1; // Track which section is expanded

  @override
  void initState() {
    super.initState();
    caseDataFuture = fetchCaseData();
  }

  /// Fetches clinical case detailed data from the API
  /// API Endpoint: GET /api/v1/notes/topics/{topic_id}/modules/
  Future<Map<String, dynamic>> fetchCaseData() async {
    try {
      // For demo, we'll use a mock API call
      // In real implementation, you'd pass the topic_id
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrl}/notes/topics/1/modules/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      print('Clinical Case Detail API Response Status: ${response.statusCode}');
      print('Clinical Case Detail API Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        if (data['status'] == 'success' && data['data'] != null) {
          print('Successfully fetched clinical case detail from API');
          return data['data'];
        } else {
          print('API Response structure unexpected: $data');
          throw Exception('Invalid API response structure');
        }
      } else {
        print('API Error: ${response.statusCode} - ${response.body}');
        throw Exception(
            'Failed to load clinical case detail: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching clinical case detail: $e');
      // Return default data structure if API fails
      return {
        'sections': [
          {
            'id': 1,
            'title': 'Gather Equipments',
            'content':
                '• Dental mirror\n• Tongue depressor\n• Gauze\n• Gloves\n• Light source\n• Patient chair',
            'is_expanded': false,
          },
          {
            'id': 2,
            'title': 'Introduction',
            'content':
                '• Introduce yourself to the patient\n• Explain the procedure\n• Obtain consent\n• Position the patient comfortably\n• Wash hands and wear gloves',
            'is_expanded': false,
          },
          {
            'id': 3,
            'title': 'General Inspection',
            'content':
                '• Observe patient\'s general appearance\n• Check for any obvious abnormalities\n• Note facial symmetry\n• Look for any swelling or discoloration\n• Assess patient\'s comfort level',
            'is_expanded': false,
          },
          {
            'id': 4,
            'title': 'Closer Inspection',
            'content':
                '• Examine lips for lesions or abnormalities\n• Check buccal mucosa\n• Inspect tongue and floor of mouth\n• Examine hard and soft palate\n• Look at oropharynx',
            'is_expanded': false,
          },
          {
            'id': 5,
            'title': 'Palpation',
            'content':
                '• Palpate lymph nodes\n• Check for tenderness\n• Assess mobility of structures\n• Feel for any masses or swelling\n• Test sensation if needed',
            'is_expanded': false,
          },
          {
            'id': 6,
            'title': 'Final Examination',
            'content':
                '• Summarize findings\n• Document any abnormalities\n• Plan further investigations if needed\n• Provide patient education\n• Thank the patient',
            'is_expanded': false,
          },
          {
            'id': 7,
            'title': 'References',
            'content':
                '• Clinical Examination Guidelines\n• Medical Textbooks\n• Professional Standards\n• Evidence-based Practice\n• Latest Research Papers',
            'is_expanded': false,
          },
        ],
        'table_of_contents': [
          'Gather Equipments',
          'Introduction',
          'General Inspection',
          'Closer Inspection',
          'Palpation',
          'Final Examination',
          'References',
        ],
      };
    }
  }

  /// Builds the banner image section
  Widget _buildBannerSection() {
    return Container(
      height: 200,
      margin: EdgeInsets.symmetric(horizontal: 20),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            offset: Offset(0, 4),
          ),
        ],
      ),
      child: Stack(
        children: [
          // Banner Image
          ClipRRect(
            borderRadius: BorderRadius.circular(12),
            child: Image.asset(
              'assets/oral_cavity.png',
              width: double.infinity,
              height: 200,
              fit: BoxFit.cover,
              errorBuilder: (context, error, stackTrace) {
                return Container(
                  width: double.infinity,
                  height: 200,
                  color: grey1,
                  child: Icon(
                    Icons.medical_services,
                    size: 64,
                    color: primaryColor,
                  ),
                );
              },
            ),
          ),
          // Dark overlay
          Container(
            width: double.infinity,
            height: 200,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  Colors.black.withOpacity(0.3),
                  Colors.black.withOpacity(0.6),
                ],
              ),
            ),
          ),
          // Text overlay
          Positioned(
            bottom: 20,
            left: 20,
            right: 20,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  widget.caseTitle.split(' ').take(2).join(' '),
                  style: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 24,
                    fontWeight: FontWeight.w700,
                    color: whiteColor,
                  ),
                ),
                Text(
                  widget.caseTitle.split(' ').skip(2).join(' '),
                  style: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 20,
                    fontWeight: FontWeight.w600,
                    color: whiteColor,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  widget.doctorName,
                  style: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 16,
                    fontWeight: FontWeight.w500,
                    color: whiteColor.withOpacity(0.9),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  /// Builds the table of contents section
  Widget _buildTableOfContents(List<String> contents) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: ExpansionTile(
        initiallyExpanded: _expandedIndex == 0,
        onExpansionChanged: (expanded) {
          setState(() {
            _expandedIndex = expanded ? 0 : -1;
          });
        },
        title: Row(
          children: [
            Text(
              'Table of contents',
              style: TextStyle(
                fontFamily: 'Poppins',
                fontSize: 18,
                fontWeight: FontWeight.w700,
                color: primaryColor,
              ),
            ),
            Spacer(),
            Icon(
              _expandedIndex == 0
                  ? Icons.keyboard_arrow_up
                  : Icons.keyboard_arrow_down,
              color: primaryColor,
            ),
          ],
        ),
        children: [
          Padding(
            padding: EdgeInsets.fromLTRB(16, 0, 16, 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: contents.asMap().entries.map((entry) {
                int index = entry.key;
                String content = entry.value;
                return Padding(
                  padding: EdgeInsets.symmetric(vertical: 4),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '${index + 1}. ',
                        style: TextStyle(
                          fontFamily: 'Poppins',
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          color: primaryColor,
                        ),
                      ),
                      Expanded(
                        child: Text(
                          content,
                          style: TextStyle(
                            fontFamily: 'Poppins',
                            fontSize: 16,
                            fontWeight: FontWeight.w500,
                            color: titlecolor,
                            decoration: TextDecoration.underline,
                            decorationColor: primaryColor,
                          ),
                        ),
                      ),
                    ],
                  ),
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }

  /// Builds individual content sections
  Widget _buildContentSection(Map<String, dynamic> section, int index) {
    final isExpanded = _expandedIndex == index;

    return Container(
      margin: EdgeInsets.symmetric(horizontal: 20, vertical: 4),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: ExpansionTile(
        initiallyExpanded: isExpanded,
        onExpansionChanged: (expanded) {
          setState(() {
            _expandedIndex = expanded ? index : -1;
          });
        },
        title: Text(
          section['title'] ?? 'Unknown Section',
          style: TextStyle(
            fontFamily: 'Poppins',
            fontSize: 18,
            fontWeight: FontWeight.w700,
            color: primaryColor,
          ),
        ),
        trailing: Icon(
          isExpanded ? Icons.keyboard_arrow_up : Icons.keyboard_arrow_down,
          color: primaryColor,
        ),
        children: [
          Padding(
            padding: EdgeInsets.fromLTRB(16, 0, 16, 16),
            child: Text(
              section['content'] ?? 'No content available',
              style: TextStyle(
                fontFamily: 'Poppins',
                fontSize: 16,
                fontWeight: FontWeight.w400,
                color: titlecolor,
                height: 1.5,
              ),
            ),
          ),
        ],
      ),
    );
  }

  /// Builds bottom navigation bar
  Widget _buildBottomNavigation() {
    return Container(
      height: 250,
      decoration: BoxDecoration(
        color: primaryColor,
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(20),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildNavItem(0, 'assets/frame.png', 'Profile'),
          _buildNavItem(1, 'assets/diamonds.png', 'Diamond'),
          _buildNavItem(2, 'assets/Group 98.png', 'Y'),
          _buildNavItem(3, 'assets/book.png', 'Notes', isActive: true),
          _buildNavItem(4, 'assets/airplane.png', 'Travel'),
        ],
      ),
    );
  }

  /// Builds individual navigation items
  Widget _buildNavItem(int index, String iconPath, String label,
      {bool isActive = false}) {
    return GestureDetector(
      onTap: () {
        setState(() {
          _selectedIndex = index;
        });
      },
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          ImageIcon(
            AssetImage(iconPath),
            color: isActive ? secondaryColor : whiteColor,
            size: 24,
          ),
          if (isActive)
            Container(
              margin: EdgeInsets.only(top: 4),
              height: 2,
              width: 20,
              decoration: BoxDecoration(
                color: secondaryColor,
                borderRadius: BorderRadius.circular(1),
              ),
            ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: color3,
      appBar: AppBar(
        backgroundColor: primaryColor,
        title: Text(
          widget.caseTitle,
          style: TextStyle(
            fontFamily: 'Poppins',
            fontSize: 20,
            fontWeight: FontWeight.w600,
            color: whiteColor,
          ),
        ),
        centerTitle: true,
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: whiteColor),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        actions: [
          IconButton(
            icon: Icon(Icons.share, color: whiteColor),
            onPressed: () {
              // TODO: Implement share functionality
            },
          ),
        ],
      ),
      body: SafeArea(
        child: FutureBuilder<Map<String, dynamic>>(
          future: caseDataFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CircularProgressIndicator(
                      color: primaryColor,
                      strokeWidth: 2,
                    ),
                    SizedBox(height: 16),
                    Text(
                      'Loading Clinical Case...',
                      style: TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 16,
                        color: grey3,
                      ),
                    ),
                  ],
                ),
              );
            }

            if (snapshot.hasError) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.error_outline,
                      size: 48,
                      color: grey3,
                    ),
                    SizedBox(height: 16),
                    Text(
                      'Failed to load content',
                      style: TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 16,
                        color: grey3,
                      ),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Please check your connection',
                      style: TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 14,
                        color: grey3,
                      ),
                    ),
                    SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: () {
                        setState(() {
                          caseDataFuture = fetchCaseData();
                        });
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: primaryColor,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                      child: Text(
                        'Retry',
                        style: TextStyle(
                          fontFamily: 'Poppins',
                          color: whiteColor,
                          fontSize: 14,
                        ),
                      ),
                    ),
                  ],
                ),
              );
            }

            final data = snapshot.data ?? {};
            final sections =
                List<Map<String, dynamic>>.from(data['sections'] ?? []);
            final tableOfContents =
                List<String>.from(data['table_of_contents'] ?? []);

            return SingleChildScrollView(
              padding: EdgeInsets.symmetric(vertical: 8),
              child: Column(
                children: [
                  _buildBannerSection(),
                  SizedBox(height: 16),
                  _buildTableOfContents(tableOfContents),
                  ...sections.asMap().entries.map((entry) {
                    int index = entry.key +
                        1; // +1 because table of contents is at index 0
                    Map<String, dynamic> section = entry.value;
                    return _buildContentSection(section, index);
                  }),
                ],
              ),
            );
          },
        ),
      ),
      bottomNavigationBar: BottomButton(onTap: () {}, selectedIndex: 3),
    );
  }
}
