import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import '../../../_env/env.dart';

class profileuniversity extends StatefulWidget {
  const profileuniversity({super.key});

  @override
  _profileuniversityState createState() => _profileuniversityState();
}

class _profileuniversityState extends State<profileuniversity> {
  List<University> universities = [];
  bool isLoading = true;
  bool hasError = false;
  String errorMessage = '';

  @override
  void initState() {
    super.initState();
    fetchFavouriteUniversities();
  }

  Future<void> fetchFavouriteUniversities() async {
    setState(() {
      isLoading = true;
      hasError = false;
    });

    try {
      final response = await http.get(
        Uri.parse(BaseUrl.favouriteUniversities),
        headers: {
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData = json.decode(response.body);
        if (responseData['status'] == 'success') {
          final List<dynamic> data = responseData['data'];
          setState(() {
            universities = data
                .map((universityData) =>
                    University.fromJson(universityData['university']))
                .toList();
            isLoading = false;
          });
        } else {
          setState(() {
            hasError = true;
            errorMessage =
                responseData['message'] ?? 'Failed to load universities';
            isLoading = false;
          });
        }
      } else {
        setState(() {
          hasError = true;
          errorMessage = 'Failed to load universities (${response.statusCode})';
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

  Future<void> removeFromFavourites(int universityId) async {
    try {
      final response = await http.delete(
        Uri.parse(BaseUrl.favouriteUniversities),
        headers: {
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'university_id': universityId,
        }),
      );

      if (response.statusCode == 200) {
        // Remove from local list
        setState(() {
          universities.removeWhere((uni) => uni.id == universityId);
        });

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('University removed from favourites'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to remove university'),
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
      backgroundColor: color3,
      body: RefreshIndicator(
        onRefresh: fetchFavouriteUniversities,
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
              'Loading your favourite universities...',
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
              'Error loading universities',
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
              onPressed: fetchFavouriteUniversities,
              style: ElevatedButton.styleFrom(
                backgroundColor: Cprimary,
              ),
              child: Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (universities.isEmpty) {
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
              'No favourite universities yet',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Cprimary,
              ),
            ),
            vGap(10),
            Text(
              'Start exploring universities and add them to your favourites!',
              style: TextStyle(
                fontSize: 14,
                color: grey3,
              ),
              textAlign: TextAlign.center,
            ),
            vGap(20),
            ElevatedButton(
              onPressed: () {
                // Navigate to universities list
                Navigator.pushNamed(context, '/universities');
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Cprimary,
              ),
              child: Text('Explore Universities'),
            ),
          ],
        ),
      );
    }

    return ListView.builder(
      itemCount: universities.length,
      itemBuilder: (context, index) {
        final University university = universities[index];
        return Padding(
          padding: const EdgeInsets.all(12.0),
          child: Card(
            semanticContainer: true,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(15),
            ),
            elevation: 1,
            child: Padding(
              padding: const EdgeInsets.all(18.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          alignment: Alignment.topLeft,
                          width: getWidth(context) / 6,
                          height: getHeight(context) / 15,
                          child: (university.logo != null &&
                                  university.logo!.isNotEmpty)
                              ? Image.network(
                                  university.logo!,
                                  fit: BoxFit.contain,
                                  errorBuilder: (context, error, stackTrace) {
                                    return Container(
                                      decoration: BoxDecoration(
                                        color: Colors.red,
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                      child: Center(
                                        child: Icon(
                                          Icons.school,
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
                                      Icons.school,
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
                                university.name,
                                style: TextStyle(
                                  fontSize: 16,
                                  fontFamily: 'Roboto',
                                  color: Cprimary,
                                  fontWeight: FontWeight.w500,
                                ),
                                maxLines: 2,
                                overflow: TextOverflow.ellipsis,
                              ),
                              Text(
                                "${university.city}, ${university.country}",
                                style: TextStyle(
                                  fontSize: 14,
                                  fontFamily: 'Roboto',
                                  color: grey3,
                                  fontWeight: FontWeight.w400,
                                ),
                              ),
                              vGap(5),
                              if (university.foundedYear != null)
                                Text(
                                  "Estd : ${university.foundedYear}",
                                  style: TextStyle(
                                    fontSize: 12,
                                    fontFamily: 'Roboto',
                                    color: grey3,
                                    fontWeight: FontWeight.w500,
                                  ),
                                ),
                              vGap(5),
                              Row(
                                children: [
                                  Text(
                                    university.universityType ?? "University",
                                    style: TextStyle(
                                      fontFamily: 'Roboto',
                                      fontSize: 12,
                                      color: grey3,
                                      fontWeight: FontWeight.w400,
                                    ),
                                  ),
                                  hGap(10),
                                  RatingBar.builder(
                                    initialRating:
                                        university.averageRating ?? 0.0,
                                    minRating: 1,
                                    direction: Axis.horizontal,
                                    allowHalfRating: true,
                                    itemCount: 5,
                                    itemSize: 10,
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
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      IconButton(
                        onPressed: () => removeFromFavourites(university.id),
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
                          // Navigate to university details
                          // Navigator.push(
                          //   context,
                          //   MaterialPageRoute(
                          //     builder: (context) => UniversityDetailsScreen(university: university),
                          //   ),
                          // );
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
                      ),
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

class University {
  final int id;
  final String name;
  final String? shortName;
  final String country;
  final String city;
  final String? logo;
  final int? foundedYear;
  final String? universityType;
  final double? averageRating;
  final String? description;
  final String? website;
  final String? email;
  final String? phone;

  University({
    required this.id,
    required this.name,
    this.shortName,
    required this.country,
    required this.city,
    this.logo,
    this.foundedYear,
    this.universityType,
    this.averageRating,
    this.description,
    this.website,
    this.email,
    this.phone,
  });

  factory University.fromJson(Map<String, dynamic> json) {
    return University(
      id: json['id'] ?? 0,
      name: json['name'] ?? '',
      shortName: json['short_name'],
      country: json['country'] ?? '',
      city: json['city'] ?? '',
      logo: json['logo'],
      foundedYear: json['founded_year'],
      universityType: json['university_type'],
      averageRating: json['average_rating']?.toDouble(),
      description: json['description'],
      website: json['website'],
      email: json['email'],
      phone: json['phone'],
    );
  }
}
