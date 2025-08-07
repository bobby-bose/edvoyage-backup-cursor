import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:http/http.dart' as http;

class Scholarship {
  final int id;
  final String title;
  final String description;
  final String image;

  Scholarship({
    required this.id,
    required this.title,
    required this.description,
    required this.image,
  });

  factory Scholarship.fromJson(Map<String, dynamic> json) {
    return Scholarship(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      image: json['image'],
    );
  }
}

class ScholarshipScreen extends StatefulWidget {
  const ScholarshipScreen({super.key});

  @override
  State<ScholarshipScreen> createState() => _ScholarshipScreenState();
}

class _ScholarshipScreenState extends State<ScholarshipScreen> {
  List<Scholarship> scholarships = List.empty();
  @override
  void initState() {
    super.initState();
    homescreennotifications();
  }

  Future<bool> homescreennotifications() async {
    final response = await http.get(
      Uri.parse(BaseUrl.scholarships),
    );

    if (response.statusCode == 200) {
      // Handle success
      print('Successfully called the scholarships');
      // You can parse and use the response data here if needed
      print(response.body);
      String jsonData = response.body;

      List<dynamic> jsonList = json.decode(jsonData);
      setState(() => scholarships =
          jsonList.map((json) => Scholarship.fromJson(json)).toList());

      print("The length of the scholarships");
      print(scholarships.length);

      return true;
    } else {
      // Handle failure
      print('Failed to called the scholarships');
      throw Exception(
          'Exception raised while called the scholarships'); // You can customize the exception message
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Scholarships'),
        backgroundColor: Cprimary,
        leading: IconButton(
          icon: Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: ListView.builder(
        itemCount: scholarships.length,
        itemBuilder: (context, index) {
          Scholarship scholarship = scholarships[index];
          return Padding(
            padding: EdgeInsets.only(
              left: 8.0,
              right: 8.0,
              top: 8.0,
            ),
            child: Card(
              semanticContainer: true,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15),
              ),
              elevation: 1,
              child: Padding(
                padding: const EdgeInsets.all(10),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          children: [
                            ClipRRect(
                              borderRadius: BorderRadius.circular(
                                  30.0), // Adjust the radius as needed
                              child: Image.network(
                                scholarship.image,
                                height: 250,
                                width: 80,
                                fit: BoxFit
                                    .cover, // Ensures the image covers the entire area
                              ),
                            ),
                          ],
                        ),
                        SizedBox(
                          width: 10,
                        ),
                        Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            SizedBox(
                              width: MediaQuery.of(context).size.width -
                                  140, // Adjust width according to your layout
                              child: Text(
                                scholarship.title,
                                style: TextStyle(
                                  fontSize: 15,
                                  fontFamily: 'Roboto',
                                  color: Cprimary,
                                  fontWeight: FontWeight.w600,
                                ),

                                softWrap: true,
                                overflow: TextOverflow
                                    .visible, // Adjust overflow behavior
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
