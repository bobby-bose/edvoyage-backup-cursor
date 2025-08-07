import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class ResponsiveClinicalNotesScreen extends StatefulWidget {
  const ResponsiveClinicalNotesScreen({super.key});

  @override
  _ResponsiveClinicalNotesScreenState createState() =>
      _ResponsiveClinicalNotesScreenState();
}

class _ResponsiveClinicalNotesScreenState
    extends State<ResponsiveClinicalNotesScreen> {
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

      print(
          'Responsive Clinical Topics API Response Status: ${response.statusCode}');
      print('Responsive Clinical Topics API Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        if (data['status'] == 'success' && data['data'] != null) {
          print('Successfully fetched responsive clinical topics from API');
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
      print('Error fetching responsive clinical topics: $e');
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
  Widget _buildClinicalTopicCard(
      Map<String, dynamic> topic, BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final isTablet = screenWidth > 600;

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
      margin: EdgeInsets.symmetric(
          horizontal: isTablet ? 40 : 20, vertical: isTablet ? 8 : 4),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(isTablet ? 12 : 8),
        border: Border(
          bottom: BorderSide(
            color: grey1,
            width: 1,
          ),
        ),
        boxShadow: isTablet
            ? [
                BoxShadow(
                  color: Colors.black.withOpacity(0.05),
                  blurRadius: 10,
                  offset: Offset(0, 2),
                ),
              ]
            : null,
      ),
      child: Padding(
        padding: EdgeInsets.symmetric(
            horizontal: isTablet ? 24 : 16, vertical: isTablet ? 16 : 12),
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
                      fontSize: isTablet ? 20 : 16,
                      fontWeight: FontWeight.w500,
                      color: titlecolor,
                    ),
                  ),
                ),
              ],
            ),
            SizedBox(height: isTablet ? 6 : 4),
            Text(
              doctorName,
              style: TextStyle(
                fontFamily: 'Poppins',
                fontSize: isTablet ? 16 : 14,
                color: grey3,
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Builds bottom navigation bar
  Widget _buildBottomNavigation(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final isTablet = screenWidth > 600;

    return Container(
      height: isTablet ? 100 : 80,
      decoration: BoxDecoration(
        color: primaryColor,
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(isTablet ? 25 : 20),
          topRight: Radius.circular(isTablet ? 25 : 20),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildNavItem(0, 'assets/frame.png', 'Profile', context),
          _buildNavItem(1, 'assets/diamonds.png', 'Diamond', context),
          _buildNavItem(2, 'assets/Group 98.png', 'Y', context),
          _buildNavItem(3, 'assets/book.png', 'Notes', context, isActive: true),
          _buildNavItem(4, 'assets/airplane.png', 'Travel', context),
        ],
      ),
    );
  }

  /// Builds individual navigation items
  Widget _buildNavItem(
      int index, String iconPath, String label, BuildContext context,
      {bool isActive = false}) {
    final screenWidth = MediaQuery.of(context).size.width;
    final isTablet = screenWidth > 600;

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
            size: isTablet ? 28 : 24,
          ),
          if (isActive)
            Container(
              margin: EdgeInsets.only(top: isTablet ? 6 : 4),
              height: isTablet ? 3 : 2,
              width: isTablet ? 25 : 20,
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
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;
    final isTablet = screenWidth > 600;
    final isLandscape = screenWidth > screenHeight;

    return Scaffold(
      backgroundColor: color3,
      appBar: AppBar(
        backgroundColor: primaryColor,
        title: Text(
          'Clinical Cases',
          style: TextStyle(
            fontFamily: 'Poppins',
            fontSize: isTablet ? 20 : 16,
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
                            strokeWidth: isTablet ? 4 : 2,
                          ),
                          SizedBox(height: isTablet ? 24 : 16),
                          Text(
                            'Loading Clinical Cases...',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: isTablet ? 20 : 16,
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
                            size: isTablet ? 64 : 48,
                            color: grey3,
                          ),
                          SizedBox(height: isTablet ? 24 : 16),
                          Text(
                            'Failed to load content',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: isTablet ? 20 : 16,
                              color: grey3,
                            ),
                          ),
                          SizedBox(height: isTablet ? 12 : 8),
                          Text(
                            'Please check your connection',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: isTablet ? 16 : 14,
                              color: grey3,
                            ),
                          ),
                          SizedBox(height: isTablet ? 24 : 16),
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
                                fontSize: isTablet ? 16 : 14,
                              ),
                            ),
                          ),
                        ],
                      ),
                    );
                  }

                  final topics = snapshot.data ?? [];

                  // For landscape tablets, show cards in a grid
                  if (isTablet && isLandscape) {
                    return GridView.builder(
                      padding:
                          EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: 2,
                        childAspectRatio: 3.0,
                        crossAxisSpacing: 20,
                        mainAxisSpacing: 20,
                      ),
                      itemCount: topics.length,
                      itemBuilder: (context, index) {
                        return _buildClinicalTopicCard(topics[index], context);
                      },
                    );
                  }

                  // For portrait and mobile, show cards in a list
                  return ListView.builder(
                    padding: EdgeInsets.symmetric(vertical: 8),
                    itemCount: topics.length,
                    itemBuilder: (context, index) {
                      return _buildClinicalTopicCard(topics[index], context);
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
