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
                      // Course Name
                      Text(
                        course['name'] ?? 'Unknown Course',
                        style: TextStyle(
                          fontFamily: 'Roboto',
                          fontSize: 16,
                          color: Cprimary,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      SizedBox(height: 5),

                      // Course Code
                      if (course['code'] != null)
                        Text(
                          'Code: ${course['code']}',
                          style: TextStyle(
                            fontFamily: 'Roboto',
                            fontSize: 12,
                            color: grey3,
                            fontWeight: FontWeight.w400,
                          ),
                        ),
                      SizedBox(height: 5),

                      // University Name
                      if (course['university_name'] != null)
                        Text(
                          'University: ${course['university_name']}',
                          style: TextStyle(
                            fontFamily: 'Roboto',
                            fontSize: 12,
                            color: grey3,
                            fontWeight: FontWeight.w400,
                          ),
                        ),
                      SizedBox(height: 5),

                      // Level and Duration
                      Row(
                        children: [
                          if (course['level'] != null)
                            Expanded(
                              child: Text(
                                'Level: ${formatLevel(course['level'])}',
                                style: TextStyle(
                                  fontFamily: 'Roboto',
                                  fontSize: 12,
                                  color: grey3,
                                ),
                              ),
                            ),
                          if (course['duration'] != null)
                            Expanded(
                              child: Text(
                                'Duration: ${formatDuration(course['duration'])}',
                                style: TextStyle(
                                  fontFamily: 'Roboto',
                                  fontSize: 12,
                                  color: grey3,
                                ),
                              ),
                            ),
                        ],
                      ),
                      SizedBox(height: 5),

                      // Description
                      if (course['description'] != null ||
                          course['short_description'] != null)
                        Text(
                          course['short_description'] ??
                              course['description'] ??
                              '',
                          style: TextStyle(
                            fontFamily: 'Roboto',
                            fontSize: 13,
                          ),
                          maxLines: 3,
                          overflow: TextOverflow.ellipsis,
                        ),
                      SizedBox(height: 5),

                      // Tuition Fee and Currency
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          if (course['tuition_fee'] != null)
                            Text(
                              'Tuition: \$${course['tuition_fee']} ${course['currency'] ?? 'USD'}',
                              style: TextStyle(
                                fontFamily: 'Roboto',
                                fontSize: 12,
                                color: Cprimary,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          if (course['credits'] != null)
                            Text(
                              'Credits: ${course['credits']}',
                              style: TextStyle(
                                fontFamily: 'Roboto',
                                fontSize: 12,
                                color: grey3,
                              ),
                            ),
                        ],
                      ),

                      // Additional Information
                      if (course['average_rating'] != null ||
                          course['total_applications'] != null) ...[
                        SizedBox(height: 5),
                        Row(
                          children: [
                            if (course['average_rating'] != null)
                              Expanded(
                                child: Text(
                                  'Rating: ${course['average_rating']}/5',
                                  style: TextStyle(
                                    fontFamily: 'Roboto',
                                    fontSize: 12,
                                    color: Colors.orange,
                                  ),
                                ),
                              ),
                            if (course['total_applications'] != null)
                              Expanded(
                                child: Text(
                                  'Applications: ${course['total_applications']}',
                                  style: TextStyle(
                                    fontFamily: 'Roboto',
                                    fontSize: 12,
                                    color: grey3,
                                  ),
                                ),
                              ),
                          ],
                        ),
                      ],

                      // Status and Features
                      if (course['status'] != null ||
                          course['is_featured'] == true ||
                          course['is_popular'] == true) ...[
                        SizedBox(height: 5),
                        Row(
                          children: [
                            if (course['status'] != null)
                              Container(
                                padding: EdgeInsets.symmetric(
                                    horizontal: 8, vertical: 2),
                                decoration: BoxDecoration(
                                  color: course['status'] == 'active'
                                      ? Colors.green
                                      : Colors.grey,
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Text(
                                  course['status'].toUpperCase(),
                                  style: TextStyle(
                                    fontFamily: 'Roboto',
                                    fontSize: 10,
                                    color: Colors.white,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            if (course['is_featured'] == true) ...[
                              SizedBox(width: 8),
                              Container(
                                padding: EdgeInsets.symmetric(
                                    horizontal: 8, vertical: 2),
                                decoration: BoxDecoration(
                                  color: Colors.blue,
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Text(
                                  'FEATURED',
                                  style: TextStyle(
                                    fontFamily: 'Roboto',
                                    fontSize: 10,
                                    color: Colors.white,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ],
                            if (course['is_popular'] == true) ...[
                              SizedBox(width: 8),
                              Container(
                                padding: EdgeInsets.symmetric(
                                    horizontal: 8, vertical: 2),
                                decoration: BoxDecoration(
                                  color: Colors.orange,
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Text(
                                  'POPULAR',
                                  style: TextStyle(
                                    fontFamily: 'Roboto',
                                    fontSize: 10,
                                    color: Colors.white,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ],
                          ],
                        ),
                      ],
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
