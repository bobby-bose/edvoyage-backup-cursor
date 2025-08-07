import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'package:frontend/_env/env.dart';
import 'package:frontend/utils/colors/colors.dart';
import '../../Study_abroad-Screen/studyabroadscreen.dart';
import 'package:frontend/models/university.dart';

class ProfileApplication extends StatefulWidget {
  const ProfileApplication({super.key});

  @override
  _ProfileApplicationState createState() => _ProfileApplicationState();
}

class _ProfileApplicationState extends State<ProfileApplication> {
  late Future<List<Application>> futureApplications;

  @override
  void initState() {
    super.initState();
    futureApplications = fetchApplications();
  }

  Future<List<Application>> fetchApplications() async {
    try {
      final response =
          await http.get(Uri.parse(BaseUrl.viewallapplicationsubmit));

      print("API Response Status: ${response.statusCode}");
      print("API Response Body: ${response.body}");

      if (response.statusCode == 200) {
        final List<dynamic> responseData =
            json.decode(response.body)['results'] ?? [];
        print("API Response: $responseData"); // Add this line

        List<Application> applications =
            responseData.map((data) => Application.fromJson(data)).toList();

        return applications;
      } else {
        print("Error response: ${response.statusCode} - ${response.body}");
        throw Exception('Failed to load applications: ${response.statusCode}');
      }
    } catch (error) {
      print("Error during fetchApplications: $error");
      // Return empty list instead of throwing exception for better UX
      return [];
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: cblack10,
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(30),
          child: Center(
            child: FutureBuilder<List<Application>>(
              future: futureApplications,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        CircularProgressIndicator(
                          valueColor:
                              AlwaysStoppedAnimation<Color>(primaryColor),
                        ),
                        SizedBox(height: 16),
                        Text(
                          'Loading Applications...',
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.grey[600],
                          ),
                        ),
                      ],
                    ),
                  );
                } else if (snapshot.hasError) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.error_outline,
                          size: 64,
                          color: Colors.red[400],
                        ),
                        SizedBox(height: 16),
                        Text(
                          'Error Loading Applications',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Colors.red[600],
                          ),
                        ),
                        SizedBox(height: 8),
                        Text(
                          'Please try again later.',
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey[500],
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  );
                } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                  return Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.description_outlined,
                        size: 64,
                        color: Colors.grey[400],
                      ),
                      SizedBox(height: 16),
                      Text(
                        'No Applications Found',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.grey[600],
                        ),
                      ),
                      SizedBox(height: 8),
                      Text(
                        'You haven\'t submitted any applications yet.',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.grey[500],
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ],
                  );
                } else {
                  List<Application> applications = snapshot.data!;
                  return Column(
                    children: applications
                        .map(
                          (application) => Padding(
                            padding: const EdgeInsets.only(bottom: 16.0),
                            child: Card(
                              elevation: 8,
                              shape: RoundedRectangleBorder(
                                side: BorderSide(
                                    width: 4,
                                    color: const Color.fromARGB(
                                        255, 255, 255, 255)),
                                borderRadius: BorderRadius.circular(20.0),
                              ),
                              child: Padding(
                                padding: const EdgeInsets.all(15.0),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    // Application Number and Status
                                    Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceBetween,
                                      children: [
                                        Expanded(
                                          child: Column(
                                            crossAxisAlignment:
                                                CrossAxisAlignment.start,
                                            children: [
                                              Text(
                                                'Application: ${application.name}',
                                                style: TextStyle(
                                                  fontWeight: FontWeight.bold,
                                                  fontSize: 16,
                                                  color: Colors.black87,
                                                ),
                                              ),
                                              SizedBox(height: 4),
                                              Text(
                                                'Status: ${application.statusDisplay}',
                                                style: TextStyle(
                                                  color: Colors.green[700],
                                                  fontWeight: FontWeight.w500,
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                        Container(
                                          padding: EdgeInsets.symmetric(
                                              horizontal: 8, vertical: 4),
                                          decoration: BoxDecoration(
                                            color: Colors.blue[100],
                                            borderRadius:
                                                BorderRadius.circular(12),
                                          ),
                                          child: Text(
                                            '${application.month} ${application.year}',
                                            style: TextStyle(
                                              fontWeight: FontWeight.bold,
                                              color: Colors.blue[800],
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                    SizedBox(height: 12),

                                    // University and Program Details
                                    Container(
                                      padding: EdgeInsets.all(12),
                                      decoration: BoxDecoration(
                                        color: Colors.grey[50],
                                        borderRadius: BorderRadius.circular(8),
                                        border: Border.all(
                                            color: Colors.grey[300]!),
                                      ),
                                      child: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Row(
                                            children: [
                                              Icon(Icons.school,
                                                  color: Colors.blue[600],
                                                  size: 20),
                                              SizedBox(width: 8),
                                              Expanded(
                                                child: Text(
                                                  application.universityName
                                                          .isNotEmpty
                                                      ? application
                                                          .universityName
                                                      : 'University Name Not Available',
                                                  style: TextStyle(
                                                    fontWeight: FontWeight.w600,
                                                    fontSize: 14,
                                                    color: Colors.black87,
                                                  ),
                                                ),
                                              ),
                                            ],
                                          ),
                                          SizedBox(height: 8),
                                          Row(
                                            children: [
                                              Icon(Icons.book,
                                                  color: Colors.green[600],
                                                  size: 20),
                                              SizedBox(width: 8),
                                              Expanded(
                                                child: Text(
                                                  application.programName
                                                          .isNotEmpty
                                                      ? application.programName
                                                      : 'Program Name Not Available',
                                                  style: TextStyle(
                                                    fontWeight: FontWeight.w500,
                                                    fontSize: 13,
                                                    color: Colors.black54,
                                                  ),
                                                ),
                                              ),
                                            ],
                                          ),
                                        ],
                                      ),
                                    ),
                                    SizedBox(height: 12),

                                    // View Button
                                    Align(
                                      alignment: Alignment.center,
                                      child: ElevatedButton(
                                        style: ElevatedButton.styleFrom(
                                          foregroundColor: primaryColor,
                                          padding: EdgeInsets.symmetric(
                                              horizontal: 20, vertical: 10),
                                          textStyle: TextStyle(
                                              fontSize: 15,
                                              fontWeight: FontWeight.bold),
                                        ),
                                        onPressed: () {
                                          Navigator.push(
                                            context,
                                            MaterialPageRoute(
                                                builder: (context) =>
                                                    UniversitHomeScreen(
                                                        university: University(
                                                            id: 0,
                                                            name: '',
                                                            city: '',
                                                            country: ''))),
                                          );
                                        },
                                        child: Text("View Details"),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ),
                        )
                        .toList(),
                  );
                }
              },
            ),
          ),
        ),
      ),
    );
  }
}

class Application {
  final int id;
  final String month;
  final String year;
  final String name;
  final String emailId;
  final int user;
  final int university_id;
  final String createdBy;
  final String universityName;
  final String programName;
  final String statusDisplay;

  Application({
    required this.id,
    // university_id
    required this.university_id,
    required this.month,
    required this.year,
    required this.name,
    required this.emailId,
    required this.user,
    required this.createdBy,
    required this.universityName,
    required this.programName,
    required this.statusDisplay,
  });

  factory Application.fromJson(Map<String, dynamic> json) {
    return Application(
      id: json['id'] ?? 0,
      month: json['month'] ?? '',
      year: json['year'] ?? '',
      name: json['name'] ?? '',
      emailId: json['email_id'] ?? '',
      user: json['user'] ?? 0,
      university_id: json['university_id'] ?? 0,
      createdBy: json['created_by'] ?? '',
      universityName: json['university_name'] ?? '',
      programName: json['program_name'] ?? '',
      statusDisplay: json['status_display'] ?? '',
    );
  }
}
