import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
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
    setState(() {
      isLoading = true;
      hasError = false;
    });

    try {
      final response = await http.get(
        Uri.parse(BaseUrl.favouriteCourses),
        headers: {
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData = json.decode(response.body);
        if (responseData['status'] == 'success') {
          final List<dynamic> data = responseData['data'];
          setState(() {
            courses = data
                .map((courseData) => Course.fromJson(courseData['course']))
                .toList();
            isLoading = false;
          });
        } else {
          setState(() {
            hasError = true;
            errorMessage = responseData['message'] ?? 'Failed to load courses';
            isLoading = false;
          });
        }
      } else {
        setState(() {
          hasError = true;
          errorMessage = 'Failed to load courses (${response.statusCode})';
          isLoading = false;
        });
      }
    } catch (e) {
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
      return Center(
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
      );
    }

    return ListView.builder(
      itemCount: courses.length,
      itemBuilder: (context, index) {
        final Course course = courses[index];
        return Padding(
          padding: const EdgeInsets.all(12),
          child: Card(
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
            elevation: 1,
            child: Padding(
              padding: const EdgeInsets.all(15.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Row(
                      children: [
                        Container(
                          alignment: Alignment.topLeft,
                          width: getWidth(context) / 6,
                          height: getHeight(context) / 15,
                          child: (course.image.isNotEmpty)
                              ? Image.network(
                                  course.image,
                                  fit: BoxFit.contain,
                                  errorBuilder: (context, error, stackTrace) {
                                    return Container(
                                      decoration: BoxDecoration(
                                        color: Colors.red,
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                      child: Center(
                                        child: Icon(
                                          Icons.book,
                                          color: Colors.white,
                                          size: 24,
                                        ),
                                      ),
                                    );
                                  },
                                )
                              : Container(
                                  decoration: BoxDecoration(
                                    color: Colors.red,
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Center(
                                    child: Icon(
                                      Icons.book,
                                      color: Colors.white,
                                      size: 24,
                                    ),
                                  ),
                                ),
                        ),
                        vGap(10),
                        Expanded(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                course.name,
                                style: TextStyle(
                                  fontFamily: 'Roboto',
                                  fontSize: 16,
                                  color: Cprimary,
                                  fontWeight: FontWeight.w500,
                                ),
                                maxLines: 2,
                                overflow: TextOverflow.ellipsis,
                              ),
                              Text(
                                course.universityName,
                                style: TextStyle(
                                  fontSize: 12,
                                  fontFamily: 'Roboto',
                                  color: Cprimary,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                              Text(
                                "${course.universityCity}, ${course.universityCountry}",
                                style: TextStyle(
                                  fontFamily: 'Roboto',
                                  fontSize: 10,
                                  color: grey3,
                                  fontWeight: FontWeight.w400,
                                ),
                              ),
                              vGap(5),
                              Row(
                                children: [
                                  Text(
                                    course.level,
                                    style: TextStyle(
                                      fontSize: 10,
                                      color: grey3,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                  Text(
                                    " • ${course.duration}",
                                    style: TextStyle(
                                      fontSize: 10,
                                      color: grey3,
                                      fontWeight: FontWeight.w400,
                                    ),
                                  ),
                                  if (course.tuitionFee > 0)
                                    Text(
                                      " • \$${course.tuitionFee.toStringAsFixed(0)}",
                                      style: TextStyle(
                                        fontSize: 10,
                                        color: grey3,
                                        fontWeight: FontWeight.w500,
                                      ),
                                    ),
                                ],
                              ),
                              vGap(5),
                              if (course.averageRating != null &&
                                  course.averageRating! > 0)
                                Row(
                                  children: [
                                    RatingBar.builder(
                                      initialRating: course.averageRating!,
                                      minRating: 1,
                                      direction: Axis.horizontal,
                                      allowHalfRating: true,
                                      itemCount: 5,
                                      itemSize: 8,
                                      itemPadding: const EdgeInsets.symmetric(
                                          horizontal: 0),
                                      itemBuilder: (context, _) => Icon(
                                        Icons.star,
                                        color: Colors.amber,
                                      ),
                                      onRatingUpdate: (rating) {
                                        // Rating update logic can be added here
                                      },
                                    ),
                                    hGap(5),
                                    Text(
                                      "(${course.totalApplications ?? 0} applications)",
                                      style: TextStyle(
                                        fontSize: 8,
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
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      IconButton(
                        onPressed: () => removeFromFavourites(course.id),
                        icon: Icon(
                          Icons.favorite,
                          color: Colors.red,
                          size: 20,
                        ),
                        tooltip: 'Remove from favourites',
                      ),
                      vGap(10),
                      ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => CourseDetails(),
                            ),
                          );
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: secondaryColor,
                          elevation: 2.0,
                          textStyle: TextStyle(
                            fontFamily: 'Roboto',
                            color: Colors.white,
                          ),
                        ),
                        child: const Text('View'),
                      )
                    ],
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
  final String universityCity;
  final String level;
  final String duration;
  final double tuitionFee;
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
    required this.universityCity,
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
      universityCity: json['university_city'] ?? '',
      level: json['level'] ?? '',
      duration: json['duration'] ?? '',
      tuitionFee: (json['tuition_fee'] ?? 0).toDouble(),
      currency: json['currency'] ?? 'USD',
      image: json['image'],
      status: json['status'] ?? 'active',
      isFeatured: json['is_featured'] ?? false,
      isPopular: json['is_popular'] ?? false,
      averageRating: json['average_rating']?.toDouble(),
      totalApplications: json['total_applications'],
      subjectsCount: json['subjects_count'],
    );
  }
}
