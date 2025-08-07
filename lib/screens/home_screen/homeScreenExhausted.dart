import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/screens/home_screen/MCQQuestionWidget.dart';
import 'package:frontend/utils/responsive.dart';
import 'package:frontend/widgets/botttom_nav.dart';
import 'package:frontend/utils/avatar.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/widgets/long_button.dart';
import 'package:frontend/screens/exploreUniversity_screen/exploreUniversitiesScreen.dart';
import 'package:frontend/screens/notification/notification.dart';
import 'package:frontend/screens/home_screen/exhausted _splash.dart';
import 'package:frontend/screens/home_screen/happy_splash.dart';
import 'package:frontend/screens/home_screen/sad_splash.dart';
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

class HomeScreenExhausted extends StatefulWidget {
  const HomeScreenExhausted({super.key});

  @override
  State<HomeScreenExhausted> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreenExhausted> {
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
              height: 200, // Set the height of the container
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
                      padding: EdgeInsets.only(top: 5),
                      height: size?.hp(26),
                      width: size?.wp(95),
                      decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(30),
                          color: Color.fromRGBO(192, 235, 231, 1),
                          border: Border.all(color: thirdColor, width: 1.5)),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          Text(
                            'How are you feeling today?',
                            style: TextStyle(
                                color: primaryColor,
                                fontWeight: FontWeight.bold),
                          ),
                          Stack(children: [
                            Container(
                              margin: EdgeInsets.only(top: 5),
                              height: size?.hp(15),
                              width: size?.wp(95),
                              child: Image.asset(
                                'assets/curving.png',
                                fit: BoxFit.fill,
                              ),
                            ),
                            Container(
                              margin: EdgeInsets.symmetric(vertical: 20),
                              padding: EdgeInsets.symmetric(horizontal: 15),
                              child: Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  SizedBox(
                                    height: size?.hp(10),
                                    width: size?.wp(17.5),
                                    child: TextButton(
                                      onPressed: () {
                                        Navigator.push(
                                            context,
                                            PageRouteBuilder(
                                                pageBuilder: (_, __, ___) =>
                                                    ExhuastedSplash()));
                                      },
                                      child: Image.asset(
                                          'assets/exhaustedB.png',
                                          fit: BoxFit.fill),
                                    ),
                                  ),
                                  Container(
                                    height: size?.hp(11),
                                    width: size?.wp(25),
                                    decoration: BoxDecoration(
                                      color: thirdColor,
                                      shape: BoxShape.circle,
                                    ),
                                    child: SizedBox(
                                      height: size?.hp(10),
                                      width: size?.wp(22),
                                      child: TextButton(
                                        onPressed: () {
                                          Navigator.push(
                                              context,
                                              PageRouteBuilder(
                                                  pageBuilder: (_, __, ___) =>
                                                      HappySplash()));
                                        },
                                        child: Image.asset(
                                          'assets/happy.png',
                                          fit: BoxFit.fill,
                                        ),
                                      ),
                                    ),
                                  ),
                                  SizedBox(
                                    height: size?.hp(10),
                                    width: size?.wp(17.5),
                                    child: TextButton(
                                        onPressed: () {
                                          Navigator.push(
                                              context,
                                              PageRouteBuilder(
                                                  pageBuilder: (_, __, ___) =>
                                                      SadSplash()));
                                        },
                                        child: Image.asset('assets/sadB.png',
                                            fit: BoxFit.fill)),
                                  )
                                ],
                              ),
                            )
                          ]),
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.end,
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Container(
                                margin: EdgeInsets.symmetric(horizontal: 2),
                                height: 10,
                                width: 2,
                                decoration: BoxDecoration(
                                    color: primaryColor,
                                    borderRadius: BorderRadius.circular(.25)),
                              ),
                              Container(
                                height: 15,
                                width: 3,
                                decoration: BoxDecoration(
                                    color: secondaryColor,
                                    borderRadius: BorderRadius.circular(.25)),
                              ),
                              Container(
                                margin: EdgeInsets.symmetric(horizontal: 2),
                                height: 10,
                                width: 2,
                                decoration: BoxDecoration(
                                    color: primaryColor,
                                    borderRadius: BorderRadius.circular(.25)),
                              )
                            ],
                          ),
                          Text(
                            'Happy',
                            style: TextStyle(
                                color: primaryColor,
                                fontWeight: FontWeight.bold),
                          )
                        ],
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
                                      'Universiteis',
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

Widget buildOption(
  String choiceLetter,
  String choiceText,
  // bool  isCorrect,
  // bool isSelected,
) {
  // Color optionColor = isSelected
  //     ? (isCorrect ? Colors.green : Colors.red)
  //     : Colors.black; // Set color based on selection and correctness

  return Padding(
    padding: EdgeInsets.all(7.0),
    child: GestureDetector(
      onTap: () {},
      child: Container(
        height: 50, // Replace with your desired height
        decoration: BoxDecoration(
          borderRadius: BorderRadius.all(Radius.circular(10)),
          border: Border.all(
            color: Colors.grey,
            width: 0.6,
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: RichText(
                  text: TextSpan(
                    children: <TextSpan>[
                      TextSpan(
                        text: '$choiceLetter - ',
                        style: TextStyle(
                          fontSize: 15,
                          color: Colors.black,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      TextSpan(
                        text: choiceText, // Replace with your option text
                        style: TextStyle(
                          fontSize: 15,
                          color: Colors.black,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    ),
  );
}

// MCQ Section
