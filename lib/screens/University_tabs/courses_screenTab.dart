import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';

class CoursesScreenTab extends StatefulWidget {
  final int universityId;

  const CoursesScreenTab({super.key, required this.universityId});
  @override
  State<CoursesScreenTab> createState() => _CoursesScreenTabState();
}

class _CoursesScreenTabState extends State<CoursesScreenTab> {
  late Future<List<dynamic>> coursesFuture;
  late Map<int, bool> favouriteStatus = {};
  @override
  void initState() {
    super.initState();
    coursesFuture = fetchCourses(widget.universityId);
  }

  Future<List<dynamic>> fetchCourses(int universityId) async {
    try {
      print('🔍 DEBUG: Fetching courses for university ID: $universityId');

      // Use the correct courses API endpoint
      final response = await http.get(
        Uri.parse('${BaseUrl.allCourses}?university_id=$universityId'),
      );

      print('🔍 DEBUG: Courses API Response Status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('🔍 DEBUG: Courses API Response Data: ${data.toString()}');

        // Handle different response structures
        if (data is Map && data.containsKey('results')) {
          print(
              '🔍 DEBUG: Found courses in results field: ${data['results'].length} courses');
          return data['results'];
        } else if (data is Map && data.containsKey('data')) {
          print(
              '🔍 DEBUG: Found courses in data field: ${data['data'].length} courses');
          return data['data'];
        } else if (data is List) {
          print(
              '🔍 DEBUG: Found courses as direct list: ${data.length} courses');
          return data;
        } else {
          print('🔍 DEBUG: No courses found in response');
          return [];
        }
      } else {
        print(
            '🔍 DEBUG: API request failed with status: ${response.statusCode}');
        throw Exception('Failed to load courses: HTTP ${response.statusCode}');
      }
    } catch (e) {
      print('🔍 DEBUG: Error fetching courses: $e');
      throw Exception('Failed to load courses: $e');
    }
  }

  String formatDuration(String? duration) {
    if (duration == null) return 'N/A';

    switch (duration) {
      case '1_year':
        return '1 Year';
      case '2_years':
        return '2 Years';
      case '3_years':
        return '3 Years';
      case '4_years':
        return '4 Years';
      case '6_months':
        return '6 Months';
      case '1_semester':
        return '1 Semester';
      default:
        return duration.replaceAll('_', ' ').toUpperCase();
    }
  }

  String formatLevel(String? level) {
    if (level == null) return 'N/A';

    switch (level) {
      case 'undergraduate':
        return 'Undergraduate';
      case 'postgraduate':
        return 'Postgraduate';
      case 'phd':
        return 'PhD';
      case 'diploma':
        return 'Diploma';
      case 'certificate':
        return 'Certificate';
      default:
        return level.toUpperCase();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: color3,
      body: FutureBuilder<List<dynamic>>(
        future: coursesFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(
              child: CircularProgressIndicator(
                color: Cprimary,
              ),
            );
          } else if (snapshot.hasError) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.error_outline,
                    color: Colors.red,
                    size: 48,
                  ),
                  SizedBox(height: 16),
                  Text(
                    'Error loading courses',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.red,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    '${snapshot.error}',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            );
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.school_outlined,
                    color: Colors.grey,
                    size: 48,
                  ),
                  SizedBox(height: 16),
                  Text(
                    'No courses available',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.grey,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'This university has not added any courses yet.',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            );
          }

          final courses = snapshot.data!;
          print(
              '🔍 DEBUG: Building courses list with ${courses.length} courses');

          return ListView.builder(
            itemCount: courses.length,
            itemBuilder: (context, index) {
              final course = courses[index];
              print(
                  '🔍 DEBUG: Building course $index: ${course['name'] ?? 'Unknown'}');

              return Card(
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                elevation: 2,
                margin: EdgeInsets.all(10),
                child: Padding(
                  padding: const EdgeInsets.all(12.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Row 1: Name, Code, Rating
                      Row(
                        children: [
                          Expanded(
                            child: Text(
                              course['name'] ?? 'Unknown Course',
                              style: TextStyle(
                                fontFamily: 'Roboto',
                                fontSize: 16,
                                color: Cprimary,
                                fontWeight: FontWeight.w700,
                              ),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          if (course['code'] != null)
                            Text(
                              course['code'],
                              style: TextStyle(
                                fontSize: 12,
                                color: grey3,
                              ),
                            ),
                          SizedBox(width: 10),
                          if (course['average_rating'] != null)
                            Row(
                              children: [
                                Icon(Icons.star,
                                    size: 14, color: Colors.orange),
                                SizedBox(width: 3),
                                Text(
                                  '${course['average_rating']}/5',
                                  style: TextStyle(
                                      fontSize: 12, color: Colors.orange),
                                ),
                              ],
                            ),
                        ],
                      ),
                      SizedBox(height: 8),

                      // Row 2: University, Level
                      Row(
                        children: [
                          if (course['university_name'] != null)
                            Expanded(
                              child: Text(
                                course['university_name'],
                                style: TextStyle(fontSize: 12, color: grey3),
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                          if (course['level'] != null)
                            Expanded(
                              child: Text(
                                'Level: ${formatLevel(course['level'])}',
                                style: TextStyle(fontSize: 12, color: grey3),
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                        ],
                      ),
                      SizedBox(height: 8),

                      // Row 3: Duration, Applications
                      Row(
                        children: [
                          if (course['duration'] != null)
                            Expanded(
                              child: Text(
                                'Duration: ${formatDuration(course['duration'])}',
                                style: TextStyle(fontSize: 12, color: grey3),
                              ),
                            ),
                          if (course['total_applications'] != null)
                            Expanded(
                              child: Text(
                                'Applications: ${course['total_applications']}',
                                style: TextStyle(fontSize: 12, color: grey3),
                              ),
                            ),
                        ],
                      ),
                      SizedBox(height: 8),

                      // Row 4: Remaining details
                      if (course['short_description'] != null ||
                          course['description'] != null)
                        Text(
                          course['short_description'] ??
                              course['description'] ??
                              '',
                          style: TextStyle(fontSize: 13),
                          maxLines: 3,
                          overflow: TextOverflow.ellipsis,
                        ),
                      SizedBox(height: 8),

                      // Tuition & Credits
                      Row(
                        children: [
                          if (course['tuition_fee'] != null)
                            Expanded(
                              child: Text(
                                'Tuition: \$${course['tuition_fee']} ${course['currency'] ?? 'USD'}',
                                style: TextStyle(
                                  fontSize: 12,
                                  color: Cprimary,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                            ),
                          if (course['credits'] != null)
                            Expanded(
                              child: Text(
                                'Credits: ${course['credits']}',
                                style: TextStyle(fontSize: 12, color: grey3),
                              ),
                            ),
                        ],
                      ),
                      SizedBox(height: 8),

                      // Badges
                      SizedBox(height: 10),

                      // Action Buttons
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Wrap(
                            spacing: 8,
                            children: [
                              if (course['status'] != null)
                                Chip(
                                  label: Text(course['status'].toUpperCase(),
                                      style: TextStyle(
                                          fontSize: 10,
                                          fontWeight: FontWeight.bold,
                                          color: Colors.white)),
                                  backgroundColor: course['status'] == 'active'
                                      ? Colors.green
                                      : Colors.grey,
                                ),
                              if (course['is_featured'] == true)
                                Chip(
                                  label: Text('FEATURED',
                                      style: TextStyle(
                                          fontSize: 10,
                                          fontWeight: FontWeight.bold,
                                          color: Colors.white)),
                                  backgroundColor: Colors.blue,
                                ),
                              if (course['is_popular'] == true)
                                Chip(
                                  label: Text('POPULAR',
                                      style: TextStyle(
                                          fontSize: 10,
                                          fontWeight: FontWeight.bold,
                                          color: Colors.white)),
                                  backgroundColor: Colors.orange,
                                ),
                            ],
                          ),
                          (favouriteStatus[course['id']] ?? false)
                              ? OutlinedButton(
                                  style: ButtonStyle(
                                    backgroundColor: MaterialStateProperty.all(
                                        Colors.redAccent),
                                  ),
                                  onPressed: () async {
                                    final courseId = course['id'];
                                    final currentlyFollowed =
                                        favouriteStatus[courseId] ?? false;

                                    try {
                                      final response = await http.post(
                                        Uri.parse(
                                            'http://192.168.1.4:8000/api/v1/bookmarks/add-favourite-course/'),
                                        headers: {
                                          'Content-Type': 'application/json'
                                        },
                                        body: jsonEncode({'course': courseId}),
                                      );

                                      if (response.statusCode == 200 ||
                                          response.statusCode == 201) {
                                        final data = jsonDecode(response.body);
                                        final action = data['action'];

                                        setState(() {
                                          favouriteStatus[courseId] =
                                              (action == 'added');
                                        });

                                        ScaffoldMessenger.of(context)
                                            .showSnackBar(
                                          SnackBar(
                                            content: Text(action == 'added'
                                                ? 'Course followed'
                                                : 'Course unfollowed'),
                                          ),
                                        );
                                      } else {
                                        ScaffoldMessenger.of(context)
                                            .showSnackBar(
                                          SnackBar(
                                              content: Text(
                                                  'Failed: ${response.body}')),
                                        );
                                      }
                                    } catch (e) {
                                      ScaffoldMessenger.of(context)
                                          .showSnackBar(
                                        SnackBar(content: Text('Error: $e')),
                                      );
                                    }
                                  },
                                  child: Text(
                                    'Unfollow',
                                    style: TextStyle(color: whiteColor),
                                  ),
                                )
                              : OutlinedButton(
                                  style: ButtonStyle(
                                      backgroundColor:
                                          MaterialStateProperty.all(
                                              primaryColor)),
                                  onPressed: () async {
                                    final courseId = course['id'];
                                    final currentlyFollowed =
                                        favouriteStatus[courseId] ?? false;

                                    try {
                                      final response = await http.post(
                                        Uri.parse(
                                            'http://192.168.1.4:8000/api/v1/bookmarks/add-favourite-course/'),
                                        headers: {
                                          'Content-Type': 'application/json'
                                        },
                                        body: jsonEncode({'course': courseId}),
                                      );

                                      if (response.statusCode == 200 ||
                                          response.statusCode == 201) {
                                        final data = jsonDecode(response.body);
                                        final action = data['action'];

                                        setState(() {
                                          favouriteStatus[courseId] =
                                              (action == 'added');
                                        });

                                        ScaffoldMessenger.of(context)
                                            .showSnackBar(
                                          SnackBar(
                                            content: Text(action == 'added'
                                                ? 'Course followed'
                                                : 'Course unfollowed'),
                                          ),
                                        );
                                      } else {
                                        ScaffoldMessenger.of(context)
                                            .showSnackBar(
                                          SnackBar(
                                              content: Text(
                                                  'Failed: ${response.body}')),
                                        );
                                      }
                                    } catch (e) {
                                      ScaffoldMessenger.of(context)
                                          .showSnackBar(
                                        SnackBar(content: Text('Error: $e')),
                                      );
                                    }
                                  },
                                  child: Text('Follow',
                                      style: TextStyle(color: whiteColor)),
                                )
                        ],
                      ),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
