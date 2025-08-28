import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:frontend/widgets/botttom_nav.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import 'package:frontend/screens/home_screen/CourseDetails.dart';
import '../../../_env/env.dart';

class profilecourses extends StatefulWidget {
  const profilecourses({super.key});

  @override
  _profilecoursesState createState() => _profilecoursesState();
}

class _profilecoursesState extends State<profilecourses> {
  List<Course> courses = [];
  bool isLoading = true;
  bool hasError = false;
  String errorMessage = '';

  @override
  void initState() {
    super.initState();
    fetchFavouriteCourses();
  }

  Future<void> fetchFavouriteCourses() async {
    if (!mounted) return;
    print("🚀 DEBUG: fetchFavouriteCourses() started");

    setState(() {
      isLoading = true;
      hasError = false;
    });

    try {
      print("🌐 DEBUG: Sending request to ${BaseUrl.favouriteCourses}");
      final response = await http.get(
        Uri.parse(BaseUrl.favouriteCourses),
        headers: {'Content-Type': 'application/json'},
      );
      print("✅ DEBUG: Response received with status ${response.statusCode}");
      debugPrint("📝 DEBUG Body: ${response.body}");

      if (!mounted) return;

      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData = json.decode(response.body);
        print("📦 DEBUG: Decoded response: $responseData");

        if (responseData['status'] == 'success') {
          final List<dynamic> data = responseData['data'];
          print("🎓 DEBUG: ${data.length} courses fetched");

          if (!mounted) return;
          setState(() {
            courses = data
                .map((courseData) => Course.fromJson(courseData['course']))
                .toList();
            isLoading = false;
          });
        } else {
          print("⚠️ DEBUG: API returned failure: ${responseData['message']}");
          if (!mounted) return;
          setState(() {
            hasError = true;
            errorMessage = responseData['message'] ?? 'Failed to load courses';
            isLoading = false;
          });
        }
      } else {
        print("❌ DEBUG: Non-200 response: ${response.statusCode}");
        if (!mounted) return;
        setState(() {
          hasError = true;
          errorMessage = 'Failed to load courses (${response.statusCode})';
          isLoading = false;
        });
      }
    } catch (e, stack) {
      print("💥 DEBUG: Exception occurred: $e");
      debugPrintStack(label: "STACK TRACE", stackTrace: stack);

      if (!mounted) return;
      setState(() {
        hasError = true;
        errorMessage = 'Network error: ${e.toString()}';
        isLoading = false;
      });
    }
  }

  Future<void> removeFromFavourites(int courseId) async {
    try {
      final response = await http.delete(
        Uri.parse(BaseUrl.favouriteCourses),
        headers: {
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'course_id': courseId,
        }),
      );

      if (response.statusCode == 200) {
        // Remove from local list
        setState(() {
          courses.removeWhere((course) => course.id == courseId);
        });

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Course removed from favourites'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to remove course'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Network error: ${e.toString()}'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomNavigationBar: BottomButton(
        onTap: () {},
        selectedIndex: 0,
      ),
      backgroundColor: play,
      body: RefreshIndicator(
        onRefresh: fetchFavouriteCourses,
        child: _buildBody(),
      ),
    );
  }

  Widget _buildBody() {
    if (isLoading) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(Cprimary),
            ),
            vGap(20),
            Text(
              'Loading your favourite courses...',
              style: TextStyle(
                fontSize: 16,
                color: grey3,
                fontFamily: 'Roboto',
              ),
            ),
          ],
        ),
      );
    }

    if (hasError) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.error_outline,
              size: 64,
              color: Colors.red,
            ),
            vGap(20),
            Text(
              'Error loading courses',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Cprimary,
              ),
            ),
            vGap(10),
            Text(
              errorMessage,
              style: TextStyle(
                fontSize: 14,
                color: grey3,
              ),
              textAlign: TextAlign.center,
            ),
            vGap(20),
            ElevatedButton(
              onPressed: fetchFavouriteCourses,
              style: ElevatedButton.styleFrom(
                backgroundColor: Cprimary,
              ),
              child: Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (courses.isEmpty) {
      return SingleChildScrollView(
        physics: AlwaysScrollableScrollPhysics(),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.favorite_border,
                size: 64,
                color: grey3,
              ),
              vGap(20),
              Text(
                'No favourite courses yet',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Cprimary,
                ),
              ),
              vGap(10),
              Text(
                'Start exploring courses and add them to your favourites!',
                style: TextStyle(
                  fontSize: 14,
                  color: grey3,
                ),
                textAlign: TextAlign.center,
              ),
              vGap(20),
              ElevatedButton(
                onPressed: () {
                  // Navigate to courses list
                  Navigator.pushNamed(context, '/courses');
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Cprimary,
                ),
                child: Text('Explore Courses'),
              ),
            ],
          ),
        ),
      );
    }

    return ListView.builder(
      itemCount: courses.length,
      itemBuilder: (context, index) {
        final Course course = courses[index];
        return Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          child: Card(
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
            elevation: 3,
            shadowColor: Colors.black26,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // LEFT SIDE - Course and College Info
                  Expanded(
                    flex: 2,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          course.name,
                          style: TextStyle(
                            fontFamily: 'Roboto',
                            fontSize: 18,
                            color: Cprimary,
                            fontWeight: FontWeight.bold,
                          ),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                        SizedBox(height: 6),
                        Text(
                          course.universityName,
                          style: TextStyle(
                            fontSize: 14,
                            fontFamily: 'Roboto',
                            color: Colors.black87,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                        Text(
                          course.universityCountry,
                          style: TextStyle(
                            fontSize: 12,
                            color: grey3,
                            fontWeight: FontWeight.w400,
                          ),
                        ),
                      ],
                    ),
                  ),

                  // RIGHT SIDE - Course Details
                  Expanded(
                    flex: 1,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text(
                          course.level,
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.black87,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                        SizedBox(height: 4),
                        Text(
                          course.duration,
                          style: TextStyle(
                            fontSize: 12,
                            color: grey3,
                            fontWeight: FontWeight.w400,
                          ),
                        ),
                        SizedBox(height: 4),
                        Text(
                          "\$${course.tuitionFee}",
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.green[700],
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        SizedBox(height: 8),
                        if (course.averageRating != null &&
                            course.averageRating! > 0)
                          Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              RatingBar.builder(
                                initialRating: course.averageRating!,
                                minRating: 1,
                                direction: Axis.horizontal,
                                allowHalfRating: true,
                                itemCount: 5,
                                itemSize: 14,
                                itemBuilder: (context, _) => Icon(
                                  Icons.star,
                                  color: Colors.amber,
                                ),
                                onRatingUpdate: (rating) {},
                              ),
                              SizedBox(width: 5),
                              Text(
                                "(${course.totalApplications ?? 0})",
                                style: TextStyle(
                                  fontSize: 10,
                                  color: grey3,
                                  fontWeight: FontWeight.w400,
                                ),
                              ),
                            ],
                          ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}

class Course {
  final int id;
  final String name;
  final String code;
  final String description;
  final String shortDescription;
  final String universityName;
  final String universityCountry;

  final String level;
  final String duration;
  final String tuitionFee;
  final String currency;
  final String image;
  final String status;
  final bool isFeatured;
  final bool isPopular;
  final double? averageRating;
  final int? totalApplications;
  final int? subjectsCount;

  Course({
    required this.id,
    required this.name,
    required this.code,
    required this.description,
    required this.shortDescription,
    required this.universityName,
    required this.universityCountry,
    required this.level,
    required this.duration,
    required this.tuitionFee,
    required this.currency,
    required this.image,
    required this.status,
    required this.isFeatured,
    required this.isPopular,
    this.averageRating,
    this.totalApplications,
    this.subjectsCount,
  });

  factory Course.fromJson(Map<String, dynamic> json) {
    return Course(
      id: json['id'] ?? 0,
      name: json['name'] ?? '',
      code: json['code'] ?? '',
      description: json['description'] ?? '',
      shortDescription: json['short_description'] ?? '',
      universityName: json['university_name'] ?? '',
      universityCountry: json['university_country'] ?? '',
      level: json['level'] ?? '',
      duration: json['duration'] ?? '',
      tuitionFee: json['tuition_fee']?.toString() ?? '',
      currency: json['currency'] ?? 'USD',
      image: json['image'],
      status: json['status'] ?? 'active',
      isFeatured: json['is_featured'] ?? false,
      isPopular: json['is_popular'] ?? false,
      averageRating: json['average_rating'] != null
          ? (json['average_rating'] as num).toDouble()
          : null,
      totalApplications: json['total_applications'],
      subjectsCount: json['subjects_count'],
    );
  }
}
