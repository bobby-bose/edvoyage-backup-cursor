import 'dart:convert';
import 'package:frontend/_env/env.dart';
import 'package:flutter/material.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import 'package:frontend/widgets/tver_modal.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/models/university.dart';

// Define constants for asset paths
const String fmgeAssetPath = "assets/badge_1_(3).png";
const String badgeAssetPath = "assets/badge_1_(2).png";
const String plabAssetPath = "assets/badge 1 (1).png";
const String trophyAssetPath = "assets/trophy_1.png";
const String library = "assets/books_1.png";
const String accomodation = "assets/home.png";
const String classroom = "assets/book-reader.png";
const String lab = "assets/flask.png";
const String clinic = "assets/clinic-medical.png";
const String ground = "assets/football-american.png";

class AboutTab extends StatefulWidget {
  final University university;
  const AboutTab({super.key, required this.university});
  @override
  State<AboutTab> createState() => _AboutTabState();
}

class _AboutTabState extends State<AboutTab> {
  late Future<Map<String, dynamic>> universityFuture;

  @override
  void initState() {
    super.initState();
    universityFuture = fetchUniversityDetails(widget.university.id);
  }

  Future<Map<String, dynamic>> fetchUniversityDetails(int id) async {
    final response = await http.get(Uri.parse('${BaseUrl.universityList}$id/'));
    if (response.statusCode == 200) {
      final decoded = json.decode(response.body);
      // If the backend wraps the data in a 'data' field, extract it
      return decoded['data'] ?? decoded;
    } else {
      throw Exception('Failed to load university details');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: color3,
      body: FutureBuilder<Map<String, dynamic>>(
        future: universityFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: \\${snapshot.error}'));
          } else if (!snapshot.hasData) {
            return Center(child: Text('No data available'));
          }
          final data = snapshot.data!;
          return ListView(
            physics: AlwaysScrollableScrollPhysics(),
            children: [
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: Column(
                  children: [
                    Container(
                      padding: EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: whiteColor,
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            "About University",
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 16,
                              fontWeight: FontWeight.w700,
                              color: Cprimary,
                            ),
                          ),
                          Divider(
                            thickness: 1,
                            color: titlecolor,
                          ),
                          Padding(
                            padding: EdgeInsets.all(8.0),
                            child: Text(
                              data['description'] ?? '',
                              style: TextStyle(
                                fontFamily: 'Poppins',
                                letterSpacing: 0.5,
                                fontSize: 14,
                              ),
                            ),
                          ),
                          if (data['mission_statement'] != null) ...[
                            SizedBox(height: 10),
                            Text('Mission:',
                                style: TextStyle(fontWeight: FontWeight.bold)),
                            Text(data['mission_statement'] ?? ''),
                          ],
                          if (data['vision_statement'] != null) ...[
                            SizedBox(height: 10),
                            Text('Vision:',
                                style: TextStyle(fontWeight: FontWeight.bold)),
                            Text(data['vision_statement'] ?? ''),
                          ],
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              vGap(20),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    "--------- edvoyage --------",
                    style: TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 16,
                      fontWeight: FontWeight.w500,
                      color: grey2,
                    ),
                  ),
                ],
              ),
              vGap(80),
            ],
          );
        },
      ),
    );
  }

  Widget buildInfoCard(
    TextStyle labelTextStyle,
    String textup,
    String textdown1,
    String textdown2,
    String imageAssetPath,
  ) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Container(
          padding: const EdgeInsets.all(10.0),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            color: thirdColor,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Image.asset(
                imageAssetPath,
                height: 50,
                width: 50,
              ),
              vGap(5),
              Text(
                textup,
                style: labelTextStyle,
              ),
              vGap(5),
              Text(
                textdown1,
                style: TextStyle(
                    letterSpacing: 1,
                    fontSize: 15,
                    fontWeight: FontWeight.w500),
                //  "$textdown1\n$textdown2",
                maxLines: 2,
              ),
              Text(
                textdown2,
                style: TextStyle(
                    letterSpacing: 1,
                    fontSize: 15,
                    fontWeight: FontWeight.w500),
              )
            ],
          ),
        ),
      ),
    );
  }

  Widget buildLocationCard(String text, String imageAssetPaths) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Container(
          padding: const EdgeInsets.all(10.0),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            color: thirdColor,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Image.asset(
                imageAssetPaths,
                height: 50,
                width: 50,
              ),
              vGap(5),
              Text(
                text,
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void displayModalBottomSheet(context, int universityId) {
    showModalBottomSheet(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.only(
            topLeft: Radius.circular(30.0),
            topRight: Radius.circular(30.0),
            bottomLeft: Radius.circular(20.0),
            bottomRight: Radius.circular(20.0),
          ),
        ),
        isScrollControlled: true,
        context: context,
        builder: (BuildContext bc) {
          return Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(30),
                topRight: Radius.circular(30),
              ),
              color: whiteColor,
            ),
            // Adjust the height based on your needs, e.g., getHeight(context) / 2
            height: MediaQuery.of(context).size.height * 0.42,
            child: Column(
              children: [
                Expanded(
                  child: DropDownDemo(
                    universityId: universityId,
                    universityName:
                        "University", // You can pass actual university name if available
                  ),
                ),
              ],
            ),
          );
        });
  }
}

class displayCards extends StatelessWidget {
  const displayCards({super.key, required this.icon, required this.text});

  final Icon icon;
  final String text;

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Container(
          padding: const EdgeInsets.all(10.0),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            color: thirdColor,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              icon,
              vGap(5),
              Text(
                text,
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

Future<String> _followUniversity(int? universityId) async {
  print('${BaseUrl.universityDetails}?id=$universityId');
  final response = await http.get(
    Uri.parse('${BaseUrl.universityDetails}?id=$universityId'),
  );

  if (response.statusCode == 200) {
    // Handle success
    print('Successfully followed university About tab');
    // You can parse and use the response data here if needed
    return response.body;
  } else {
    // Handle failure
    print('Failed to follow university');
    throw Exception(
        'Failed to follow university'); // You can customize the exception message
  }
}
