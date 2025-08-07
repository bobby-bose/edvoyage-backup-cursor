import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/utils/responsive.dart';
import 'package:frontend/widgets/botttom_nav.dart';
import '../../../utils/avatar.dart';
import '../../../utils/colors/colors.dart';
import '../../../widgets/long_button.dart';
import '../../exploreUniversity_screen/exploreUniversitiesScreen.dart';
import '../../notification/notification.dart';
import '../MCQQuestionWidget.dart';
import 'package:http/http.dart' as http;

class HomeData {
  final Map<String, dynamic> questionOfTheDayData;
  final List<dynamic> allNotificationsData;
  final List<dynamic> offerNotificationsData;

  HomeData({
    required this.questionOfTheDayData,
    required this.allNotificationsData,
    required this.offerNotificationsData,
  });
}

class HomeScreenhappysplash extends StatefulWidget {
  const HomeScreenhappysplash({super.key});

  @override
  State<HomeScreenhappysplash> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreenhappysplash> {
  Measurements? size;
  HomeData? homeData;
  int universityLength = 0;

  @override
  void initState() {
    super.initState();
    // Call fetchData when the widget is first created
    fetchData();
    getLengthOfAllUniversities();
  }

  // GET THE LENGTH OF ALL THE uNIVERSITIES FROM THE API BaseUrl.universityList;
  // Fetch data from API

  Future<void> getLengthOfAllUniversities() async {
    try {
      var response = await http.get(Uri.parse(BaseUrl.universityList));
      if (response.statusCode == 200) {
        List<dynamic> responseData = json.decode(response.body);
        print("The Response Data is: $responseData");
        print('Length of University List: ${responseData.length}');

        setState(() {
          universityLength = responseData.length;
        });
      } else {
        print('Failed to load data: ${response.statusCode}');
      }
    } catch (e) {
      print('Error: $e');
    }
  }

  Future<void> fetchData() async {
    try {
      var response = await http.get(Uri.parse(BaseUrl.home));

      if (response.statusCode == 200) {
        // Parse the JSON string into a Map
        Map<String, dynamic> responseData = json.decode(response.body);

        // Accessing question_of_the_day data
        Map<String, dynamic> questionOfTheDayData =
            responseData['question_of_the_day'];
        print('Question of the day: $questionOfTheDayData');

        // Accessing all_notifications data
        List<dynamic> allNotificationsData = responseData['all_notifications'];
        print('All Notifications: $allNotificationsData');

        // Accessing offer_notifications data
        List<dynamic> offerNotificationsData =
            responseData['offer_notifications'];
        print('Offer Notifications: $offerNotificationsData');

        // Set homeData with the collected data
        setState(() {
          homeData = HomeData(
            questionOfTheDayData: questionOfTheDayData,
            allNotificationsData: allNotificationsData,
            offerNotificationsData: offerNotificationsData,
          );
        });
      } else {
        print('Failed to load data: ${response.statusCode}');
      }
    } catch (e) {
      // Handle errors here
      print('Error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return WillPopScope(
      onWillPop: () async {
        SystemNavigator.pop();
        return false;
      },
      child: Scaffold(
          bottomNavigationBar: BottomButton(onTap: () {}, selectedIndex: 2),
          backgroundColor: Colors.grey.shade200,
          appBar: AppBar(
            backgroundColor: Colors.white,
            elevation: 0.2,
            automaticallyImplyLeading: false,
            centerTitle: true,
            title: SizedBox(
              height: 250, // Set the width of the container
              width: 200, // Set the height of the container
              child: Image.asset(
                  edvoyagelogo1), // Replace with the actual image path
            ),
            actions: [
              IconButton(
                  icon: Icon(
                    Icons.notifications,
                    color: primaryColor,
                  ),
                  onPressed: () {
                    Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) => NotificationScreen()));
                  })
            ],
          ),
          body: SingleChildScrollView(
            scrollDirection: Axis.vertical,
            child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Column(children: [
                  Center(
                    child: Container(
                      alignment: Alignment.center,
                      height: size?.hp(6),
                      width: size?.wp(95),
                      decoration: BoxDecoration(
                          color: Color.fromRGBO(192, 235, 231, 1),
                          borderRadius: BorderRadius.circular(25)),
                      child: Text(
                        '"Everyday is a newday!"',
                        textScaleFactor: 1.2,
                        style: TextStyle(
                            color: primaryColor, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                  Center(
                    child: Container(
                      margin: EdgeInsets.symmetric(vertical: 10),
                      height: size?.hp(30),
                      width: size?.wp(95),
                      decoration: BoxDecoration(
                          color: thirdColor,
                          borderRadius: BorderRadius.circular(10),
                          boxShadow: [
                            BoxShadow(
                                offset: Offset(1, 1),
                                blurRadius: 2,
                                color: grey2,
                                spreadRadius: 2)
                          ]),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          Text(
                            'Explore Courses & Universities',
                            textScaleFactor: 1.6,
                            style: TextStyle(
                              color: primaryColor,
                              fontWeight: FontWeight.w800,
                            ),
                          ),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                            children: [
                              Container(
                                height: size?.hp(14),
                                width: size?.wp(42),
                                decoration: BoxDecoration(
                                    color: thirdColor,
                                    borderRadius: BorderRadius.circular(10),
                                    boxShadow: [
                                      BoxShadow(
                                          offset: Offset(0, 0),
                                          spreadRadius: 1,
                                          color: grey2)
                                    ]),
                                child: Column(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    SizedBox(
                                      height: size?.hp(4.5),
                                      width: size?.wp(9.6),
                                      child: Image.asset(
                                        universityimage,
                                      ),
                                    ),
                                    Text(
                                      universityLength.toString(),
                                      textScaleFactor: 1.5,
                                      style: TextStyle(
                                        fontWeight: FontWeight.w900,
                                      ),
                                    ),
                                    Text(
                                      'Universities',
                                      style: TextStyle(
                                        fontWeight: FontWeight.w800,
                                      ),
                                    )
                                  ],
                                ),
                              ),
                              Container(
                                height: size?.hp(14),
                                width: size?.wp(42),
                                decoration: BoxDecoration(
                                    color: thirdColor,
                                    borderRadius: BorderRadius.circular(10),
                                    boxShadow: [
                                      BoxShadow(
                                          offset: Offset(0, 0),
                                          spreadRadius: 1,
                                          color: grey2)
                                    ]),
                                child: Column(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    SizedBox(
                                      height: size?.hp(4.5),
                                      width: size?.wp(9.6),
                                      child: Image.asset(
                                        coursesimage,
                                      ),
                                    ),
                                    Text(
                                      '30,000+',
                                      textScaleFactor: 1.5,
                                      style: TextStyle(
                                        fontWeight: FontWeight.w900,
                                      ),
                                    ),
                                    Text(
                                      'Courses',
                                      style: TextStyle(
                                        fontWeight: FontWeight.w800,
                                      ),
                                    )
                                  ],
                                ),
                              )
                            ],
                          ),
                          LongButton(
                              action: () {
                                Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                        builder: (context) =>
                                            ExploreUniversitiesScreen()));
                              },
                              text: 'Explore Now'),
                        ],
                      ),
                    ),
                  ),
                  MCQQuestionWidget(),
                ])),
          )),
    );
  }
}
