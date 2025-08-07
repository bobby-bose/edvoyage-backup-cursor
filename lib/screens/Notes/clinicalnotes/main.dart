import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class ClinicalNotesScreen extends StatefulWidget {
  const ClinicalNotesScreen({super.key});

  @override
  _ClinicalNotesScreenState createState() => _ClinicalNotesScreenState();
}

class _ClinicalNotesScreenState extends State<ClinicalNotesScreen> {
  late Future<List<Map<String, dynamic>>> clinicalTopicsFuture;
  int _selectedIndex = 3; // Notes tab is active

  @override
  void initState() {
    super.initState();
    clinicalTopicsFuture = fetchClinicalTopics();
  }

  /// Fetches clinical case topics data from the API
  /// API Endpoint: GET /api/v1/notes/categories/clinical_case/topics/
  Future<List<Map<String, dynamic>>> fetchClinicalTopics() async {
    try {
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrl}/notes/categories/clinical_case/topics/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      print('Clinical Topics API Response Status: ${response.statusCode}');
      print('Clinical Topics API Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        if (data['status'] == 'success' && data['data'] != null) {
          print('Successfully fetched clinical topics from API');
          return List<Map<String, dynamic>>.from(data['data']);
        } else {
          print('API Response structure unexpected: $data');
          throw Exception('Invalid API response structure');
        }
      } else {
        print('API Error: ${response.statusCode} - ${response.body}');
        throw Exception(
            'Failed to load clinical topics: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching clinical topics: $e');
      // Return default data structure if API fails
      return [
        {
          'id': 1,
          'title': 'Oral Cavity Examination',
          'description': 'Comprehensive oral cavity examination techniques',
          'doctor_name': 'Dr. Ranchodas Chanchad',
          'is_featured': true,
          'order': 1
        },
        {
          'id': 2,
          'title': 'Auscultation Examination',
          'description': 'Heart and lung auscultation techniques',
          'doctor_name': 'Dr. Ranchodas Chanchad',
          'is_featured': false,
          'order': 2
        },
        {
          'id': 3,
          'title': 'Pneumonia Examination',
          'description': 'Diagnostic approaches for pneumonia cases',
          'doctor_name': 'Dr. Ranchodas Chanchad',
          'is_featured': false,
          'order': 3
        },
        {
          'id': 4,
          'title': 'Renal System Examination',
          'description': 'Kidney and urinary system assessment',
          'doctor_name': 'Dr. Ranchodas Chanchad',
          'is_featured': false,
          'order': 4
        },
        {
          'id': 5,
          'title': 'Heart Functioning Examination',
          'description': 'Cardiac assessment and diagnostic methods',
          'doctor_name': 'Dr. Ranchodas Chanchad',
          'is_featured': false,
          'order': 5
        },
        {
          'id': 6,
          'title': 'Retina Examination',
          'description': 'Ophthalmological retinal assessment',
          'doctor_name': 'Dr. Ranchodas Chanchad',
          'is_featured': false,
          'order': 6
        },
        {
          'id': 7,
          'title': 'Limb Examination',
          'description': 'Musculoskeletal assessment techniques',
          'doctor_name': 'Dr. Ranchodas Chanchad',
          'is_featured': false,
          'order': 7
        },
        {
          'id': 8,
          'title': 'Nervous System Examination',
          'description': 'Neurological assessment and testing',
          'doctor_name': 'Dr. Ranchodas Chanchad',
          'is_featured': false,
          'order': 8
        },
      ];
    }
  }

  /// Builds individual clinical case topic cards
  Widget _buildClinicalTopicCard(Map<String, dynamic> topic) {
    // Map of doctor names for different clinical cases
    final doctorNames = {
      'Cardiovascular Cases': 'Dr. Ranchodas Chanchad',
      'Respiratory Cases': 'Dr. Ranchodas Chanchad',
      'Gastrointestinal Cases': 'Dr. Ranchodas Chanchad',
      'Neurological Cases': 'Dr. Ranchodas Chanchad',
      'Endocrine Cases': 'Dr. Ranchodas Chanchad',
      'Renal Cases': 'Dr. Ranchodas Chanchad',
      'Hematological Cases': 'Dr. Ranchodas Chanchad',
      'Infectious Disease Cases': 'Dr. Ranchodas Chanchad',
      'Oncological Cases': 'Dr. Ranchodas Chanchad',
      'Pediatric Cases': 'Dr. Ranchodas Chanchad',
      'Obstetric Cases': 'Dr. Ranchodas Chanchad',
      'Psychiatric Cases': 'Dr. Ranchodas Chanchad',
      'Surgical Cases': 'Dr. Ranchodas Chanchad',
      'Emergency Cases': 'Dr. Ranchodas Chanchad',
      'Trauma Cases': 'Dr. Ranchodas Chanchad',
      'Critical Care Cases': 'Dr. Ranchodas Chanchad',
      'Geriatric Cases': 'Dr. Ranchodas Chanchad',
      'Rheumatological Cases': 'Dr. Ranchodas Chanchad',
      'Dermatological Cases': 'Dr. Ranchodas Chanchad',
      'Ophthalmological Cases': 'Dr. Ranchodas Chanchad',
      'ENT Cases': 'Dr. Ranchodas Chanchad',
      'Orthopedic Cases': 'Dr. Ranchodas Chanchad',
      'Urological Cases': 'Dr. Ranchodas Chanchad',
    };

    final doctorName = doctorNames[topic['title']] ?? 'Dr. Ranchodas Chanchad';

    return Container(
      margin: EdgeInsets.symmetric(horizontal: 20, vertical: 4),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(8),
        border: Border(
          bottom: BorderSide(
            color: grey1,
            width: 1,
          ),
        ),
      ),
      child: Padding(
        padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    topic['title'] ?? 'Unknown Topic',
                    style: TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 16,
                      fontWeight: FontWeight.w500,
                      color: titlecolor,
                    ),
                  ),
                ),
              ],
            ),
            SizedBox(height: 4),
            Text(
              doctorName,
              style: TextStyle(
                fontFamily: 'Poppins',
                fontSize: 14,
                color: grey3,
              ),
            ),
          ],
        ),
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
          'Clinical Cases',
          style: TextStyle(
            fontFamily: 'Poppins',
            fontSize: 20,
            fontWeight: FontWeight.w600,
            color: whiteColor,
          ),
        ),
        centerTitle: true,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios, color: whiteColor),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: FutureBuilder<List<Map<String, dynamic>>>(
                future: clinicalTopicsFuture,
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
                            'Loading Clinical Cases...',
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
                                clinicalTopicsFuture = fetchClinicalTopics();
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

                  final topics = snapshot.data ?? [];

                  return ListView.builder(
                    padding: EdgeInsets.symmetric(vertical: 8),
                    itemCount: topics.length,
                    itemBuilder: (context, index) {
                      return _buildClinicalTopicCard(topics[index]);
                    },
                  );
                },
              ),
            ),
            BottomButton(onTap: () {}, selectedIndex: 3),
          ],
        ),
      ),
    );
  }
}
