// import 'dart:convert';
// import 'package:flutter/material.dart';
// import 'package:flutter/services.dart';
// import 'package:frontend/utils/colors/colors.dart';
// import 'package:frontend/screens/Notes/mcqnotes/sub/cards.dart';

// class MCQNotesSubScreen extends StatefulWidget {
//   final String categoryTitle;
//   final int categoryId;

//   const MCQNotesSubScreen({
//     super.key,
//     required this.categoryTitle,
//     required this.categoryId,
//   });

//   @override
//   _MCQNotesSubScreenState createState() => _MCQNotesSubScreenState();
// }

// class _MCQNotesSubScreenState extends State<MCQNotesSubScreen> {
//   late Future<List<Map<String, dynamic>>> mcqModulesFuture;
//   int _selectedIndex = 3; // Notes tab is active

//   @override
//   void initState() {
//     super.initState();
//     mcqModulesFuture = fetchMCQModules();
//   }

//   /// Fetches MCQ modules data from local JSON file for development
//   Future<List<Map<String, dynamic>>> fetchMCQModules() async {
//     try {
//       // Load data from local JSON file
//       final String response = await rootBundle
//           .loadString('lib/screens/Notes/mcqnotes/sub/data.json');
//       final data = json.decode(response);

//       print('MCQ Modules JSON Response: $data');

//       if (data['status'] == 'success' && data['data'] != null) {
//         print('Successfully loaded MCQ modules from JSON file');
//         return List<Map<String, dynamic>>.from(data['data']);
//       } else {
//         print('JSON Response structure unexpected: $data');
//         throw Exception('Invalid JSON response structure');
//       }
//     } catch (e) {
//       print('Error loading MCQ modules from JSON: $e');
//       // Return default data structure if JSON fails
//       return [
//         {
//           'id': 1,
//           'title': 'Basic Anatomy MCQs',
//           'description': 'Fundamental anatomy multiple choice questions',
//           'questions_count': 25,
//           'time_limit': '30 Min',
//           'difficulty': 'Easy',
//           'accessType': 'free',
//           'moduleId': 'mcq_001'
//         },
//         {
//           'id': 2,
//           'title': 'Advanced Physiology MCQs',
//           'description': 'Complex physiology questions for advanced students',
//           'questions_count': 40,
//           'time_limit': '45 Min',
//           'difficulty': 'Hard',
//           'accessType': 'premium',
//           'moduleId': 'mcq_002'
//         },
//         {
//           'id': 3,
//           'title': 'Biochemistry Fundamentals',
//           'description': 'Core biochemistry concepts and applications',
//           'questions_count': 30,
//           'time_limit': '35 Min',
//           'difficulty': 'Medium',
//           'accessType': 'free',
//           'moduleId': 'mcq_003'
//         },
//         {
//           'id': 4,
//           'title': 'Pharmacology MCQs',
//           'description': 'Drug mechanisms and therapeutic applications',
//           'questions_count': 35,
//           'time_limit': '40 Min',
//           'difficulty': 'Medium',
//           'accessType': 'premium',
//           'moduleId': 'mcq_004'
//         },
//         {
//           'id': 5,
//           'title': 'Pathology Practice',
//           'description': 'Disease mechanisms and diagnostic approaches',
//           'questions_count': 28,
//           'time_limit': '30 Min',
//           'difficulty': 'Hard',
//           'accessType': 'free',
//           'moduleId': 'mcq_005'
//         },
//       ];
//     }
//   }

//   /// Navigate to MCQ quiz screen
//   void _navigateToMCQQuiz(Map<String, dynamic> moduleData) {
//     // TODO: Implement MCQ quiz navigation
//     print('Navigating to MCQ quiz for: ${moduleData['title']}');
//     // Navigator.push(
//     //   context,
//     //   MaterialPageRoute(
//     //     builder: (context) => MCQQuizScreen(moduleData: moduleData),
//     //   ),
//     // );
//   }

//   /// Builds bottom navigation bar
//   Widget _buildBottomNavigation() {
//     return Container(
//       height: 250,
//       decoration: BoxDecoration(
//         color: primaryColor,
//         borderRadius: BorderRadius.only(
//           topLeft: Radius.circular(20),
//           topRight: Radius.circular(20),
//         ),
//       ),
//       child: Row(
//         mainAxisAlignment: MainAxisAlignment.spaceEvenly,
//         children: [
//           _buildNavItem(0, Icons.home_outlined, 'Home'),
//           _buildNavItem(1, Icons.category_outlined, 'Categories'),
//           _buildNavItem(2, Icons.diamond_outlined, 'De Voyage'),
//           _buildNavItem(3, Icons.book, 'Notes', isActive: true),
//           _buildNavItem(4, Icons.flight, 'Travel'),
//         ],
//       ),
//     );
//   }

//   /// Builds individual navigation items
//   Widget _buildNavItem(int index, IconData icon, String label,
//       {bool isActive = false}) {
//     return GestureDetector(
//       onTap: () {
//         setState(() {
//           _selectedIndex = index;
//         });
//       },
//       child: Column(
//         mainAxisAlignment: MainAxisAlignment.center,
//         children: [
//           Icon(
//             icon,
//             color: isActive ? secondaryColor : whiteColor,
//             size: 24,
//           ),
//           if (isActive)
//             Container(
//               margin: EdgeInsets.only(top: 4),
//               height: 2,
//               width: 20,
//               decoration: BoxDecoration(
//                 color: secondaryColor,
//                 borderRadius: BorderRadius.circular(1),
//               ),
//             ),
//         ],
//       ),
//     );
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       backgroundColor: color3,
//       appBar: AppBar(
//         title: Text(widget.categoryTitle),
//         backgroundColor: primaryColor,
//         elevation: 0,
//         leading: IconButton(
//           icon: Icon(Icons.arrow_back_ios, color: whiteColor),
//           onPressed: () {
//             Navigator.pop(context);
//           },
//         ),
//       ),
//       body: SafeArea(
//         child: Column(
//           children: [
//             Expanded(
//               child: FutureBuilder<List<Map<String, dynamic>>>(
//                 future: mcqModulesFuture,
//                 builder: (context, snapshot) {
//                   if (snapshot.connectionState == ConnectionState.waiting) {
//                     return Center(
//                       child: Column(
//                         mainAxisAlignment: MainAxisAlignment.center,
//                         children: [
//                           CircularProgressIndicator(
//                             color: primaryColor,
//                             strokeWidth: 2,
//                           ),
//                           SizedBox(height: 16),
//                           Text(
//                             'Loading MCQ Modules...',
//                             style: TextStyle(
//                               fontFamily: 'Poppins',
//                               fontSize: 16,
//                               color: grey3,
//                             ),
//                           ),
//                         ],
//                       ),
//                     );
//                   }

//                   if (snapshot.hasError) {
//                     return Center(
//                       child: Column(
//                         mainAxisAlignment: MainAxisAlignment.center,
//                         children: [
//                           Icon(
//                             Icons.error_outline,
//                             size: 48,
//                             color: grey3,
//                           ),
//                           SizedBox(height: 16),
//                           Text(
//                             'Failed to load MCQ modules',
//                             style: TextStyle(
//                               fontFamily: 'Poppins',
//                               fontSize: 16,
//                               color: grey3,
//                             ),
//                           ),
//                           SizedBox(height: 8),
//                           Text(
//                             'Please check your connection',
//                             style: TextStyle(
//                               fontFamily: 'Poppins',
//                               fontSize: 14,
//                               color: grey3,
//                             ),
//                           ),
//                           SizedBox(height: 16),
//                           ElevatedButton(
//                             onPressed: () {
//                               setState(() {
//                                 mcqModulesFuture = fetchMCQModules();
//                               });
//                             },
//                             style: ElevatedButton.styleFrom(
//                               backgroundColor: primaryColor,
//                               shape: RoundedRectangleBorder(
//                                 borderRadius: BorderRadius.circular(8),
//                               ),
//                             ),
//                             child: Text(
//                               'Retry',
//                               style: TextStyle(
//                                 fontFamily: 'Poppins',
//                                 color: whiteColor,
//                                 fontSize: 14,
//                               ),
//                             ),
//                           ),
//                         ],
//                       ),
//                     );
//                   }

//                   final modules = snapshot.data ?? [];

//                   return ListView.builder(
//                     padding: EdgeInsets.symmetric(vertical: 10),
//                     physics: BouncingScrollPhysics(),
//                     itemCount: modules.length,
//                     itemBuilder: (context, index) {
//                       final module = modules[index];
//                       return MCQModuleCard(
//                         module: module,
//                         onTap: () => _navigateToMCQQuiz(module),
//                       );
//                     },
//                   );
//                 },
//               ),
//             ),
//             _buildBottomNavigation(),
//           ],
//         ),
//       ),
//     );
//   }
// }

// ======================================================================

// ======================================================================

// ======================================================================

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:frontend/widgets/botttom_nav.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/screens/Notes/mcqnotes/sub/cards.dart';

class MCQNotesSubScreen extends StatefulWidget {
  final String categoryTitle;
  final int categoryId;

  const MCQNotesSubScreen({
    super.key,
    required this.categoryTitle,
    required this.categoryId,
  });

  @override
  _MCQNotesSubScreenState createState() => _MCQNotesSubScreenState();
}

class _MCQNotesSubScreenState extends State<MCQNotesSubScreen> {
  late Future<List<Map<String, dynamic>>> mcqModulesFuture;
  int _selectedIndex = 3; // Notes tab is active

  @override
  void initState() {
    super.initState();
    mcqModulesFuture = fetchMCQModules();
  }

  /// Fetches MCQ modules data from API using the categoryId
  Future<List<Map<String, dynamic>>> fetchMCQModules() async {
    final String apiUrl =
        'http://192.168.1.4:8000/api/v1/notes/mcq/topics/${widget.categoryId}';

    try {
      final response = await http.get(Uri.parse(apiUrl));

      if (response.statusCode == 200) {
        final decoded = json.decode(response.body);
        print('MCQ Modules API Response: $decoded');
        print('Decoded response: $decoded');
        // decoded=[{id: 1, name: topic}, {id: 2, name: topic 2}]

        return decoded.map<Map<String, dynamic>>((item) {
          return {
            'id': item['id'],
            'title': item['name'],
          };
        }).toList();
      } else {
        throw Exception(
            'Failed to load modules. Status: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching MCQ modules from API: $e');
      throw Exception('Failed to fetch data');
    }
  }

  /// Navigate to MCQ quiz screen
  void _navigateToMCQQuiz(Map<String, dynamic> moduleData) {
    // TODO: Implement MCQ quiz navigation
    print('Navigating to MCQ quiz for: ${moduleData['title']}');
    // Navigator.push(
    //   context,
    //   MaterialPageRoute(
    //     builder: (context) => MCQQuizScreen(moduleData: moduleData),
    //   ),
    // );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: color3,
      appBar: AppBar(
        title: Text(widget.categoryTitle),
        backgroundColor: primaryColor,
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
                future: mcqModulesFuture,
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
                            'Loading MCQ Modules...',
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
                            'Failed to load MCQ modules',
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
                                mcqModulesFuture = fetchMCQModules();
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

                  final modules = snapshot.data ?? [];

                  return ListView.builder(
                    padding: EdgeInsets.symmetric(vertical: 10),
                    physics: BouncingScrollPhysics(),
                    itemCount: modules.length,
                    itemBuilder: (context, index) {
                      final module = modules[index];
                      return MCQModuleCard(
                        module: module,
                        onTap: () => _navigateToMCQQuiz(module),
                      );
                    },
                  );
                },
              ),
            ),
            // use the bottom navigation bar from the main screen
            BottomButton(
              onTap: () {},
              selectedIndex: _selectedIndex,
            ),
          ],
        ),
      ),
    );
  }
}
