import 'dart:async';

import 'package:flutter/material.dart';
import 'package:frontend/screens/home_screen/CourseDetails.dart';

import '../../utils/colors/colors.dart';
import '../../utils/responsive.dart';
import '../../widgets/long_button.dart';
import '../../widgets/longarrow/long_arrow.dart';
import '../../widgets/longarrow/long_arrow1.dart';
import '../../widgets/longarrow/long_arrow2.dart';
import '../../widgets/longarrow/long_arrow3.dart';
import '../../widgets/longarrow/long_arrow4.dart';
import '../../widgets/tver_modal.dart';

class coursesTab extends StatefulWidget {
  final String coursename;
  final String duration;
  final String intake;
  final int grandtotal;
  final String neetEligibility;
  final String ieltsEligibility;
  final bool passport;
  final bool ielts;
  final bool tenthCard;
  final bool twelfthCard;
  final bool visa;
  final String Firstyearfees;
  final String Secondyearfees;
  final String Thirdyearfees;
  final String Fourthyearfees;
  final String Fifthyearfees;
  final List<dynamic> Firstyearsubjects;
  final List<dynamic> Secondyearsubjects;
  final List<dynamic> Thirdyearsubjects;
  final List<dynamic> Fourthyearsubjects;
  final List<dynamic> Fifthyearsubjects;
  @override
  const coursesTab({
    super.key,
    required this.coursename,
    required this.duration,
    required this.intake,
    required this.grandtotal,
    required this.neetEligibility,
    required this.ieltsEligibility,
    required this.passport,
    required this.ielts,
    required this.tenthCard,
    required this.twelfthCard,
    required this.visa,
    required this.Firstyearfees,
    required this.Secondyearfees,
    required this.Thirdyearfees,
    required this.Fourthyearfees,
    required this.Fifthyearfees,
    required this.Firstyearsubjects,
    required this.Secondyearsubjects,
    required this.Thirdyearsubjects,
    required this.Fourthyearsubjects,
    required this.Fifthyearsubjects,
  });

  @override
  _coursesTabState createState() => _coursesTabState();
}

class _coursesTabState extends State<coursesTab> {
  TextEditingController timeinput = TextEditingController();
  TextEditingController dateinput = TextEditingController();
  @override
  void initState() {
    timeinput.text = "";
    dateinput.text = "";
    super.initState();
  }

  late int activeMeterIndex;
  final StreamController activeMeterIndexStreamControl =
      StreamController.broadcast();
  Stream get onUpdateActiveIndex => activeMeterIndexStreamControl.stream;
  void updateExpansionTile() =>
      activeMeterIndexStreamControl.sink.add(activeMeterIndex);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: color3,
      body: SingleChildScrollView(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.only(
                  left: 18, right: 18, bottom: 5, top: 10),
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(Radius.circular(12)),
                  color: Color.fromRGBO(255, 255, 255, 1),
                ),
                child: Padding(
                    padding: const EdgeInsets.all(18.0),
                    child: Row(
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              widget.coursename,
                              style: TextStyle(
                                  fontSize: 22,
                                  letterSpacing: 1,
                                  fontFamily: 'Roboto',
                                  fontWeight: FontWeight.w700,
                                  color: Cprimary),
                            ),
                            vGap(10),
                            Row(
                              children: [
                                Row(
                                  children: [
                                    Icon(
                                      Icons.access_time_outlined,
                                      size: 25,
                                      color: Cprimary,
                                    ),
                                    hGap(10),
                                    Column(
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceBetween,
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          widget.duration,
                                          style: TextStyle(
                                              fontSize: 12,
                                              fontFamily: 'Roboto',
                                              color: Cprimary,
                                              fontWeight: FontWeight.w500),
                                        ),
                                        vGap(5),
                                        Text(
                                          "Duration",
                                          style: TextStyle(
                                              fontSize: 10,
                                              fontFamily: 'Roboto',
                                              fontWeight: FontWeight.w400),
                                        )
                                      ],
                                    ),
                                  ],
                                ),
                                hGap(15),
                                Row(
                                  children: [
                                    Icon(
                                      Icons.calendar_month,
                                      size: 25,
                                      color: Cprimary,
                                    ),
                                    hGap(10),
                                    Column(
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceBetween,
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          widget.intake,
                                          style: TextStyle(
                                              fontSize: 12,
                                              fontFamily: 'Roboto',
                                              color: Cprimary,
                                              fontWeight: FontWeight.w500),
                                        ),
                                        vGap(5),
                                        Text(
                                          "Intake",
                                          style: TextStyle(
                                              fontFamily: 'Roboto',
                                              fontSize: 10,
                                              fontWeight: FontWeight.w400),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ],
                        ),
                        hGap(10),
                        Container(
                          height: 70,
                          width: 110,
                          decoration: BoxDecoration(
                            shape: BoxShape.rectangle,
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(
                              color: primaryColor, // Border color
                              width: 2, // Border width
                            ),
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(
                                "\$${widget.grandtotal}",
                                style: TextStyle(
                                    fontSize: 22,
                                    letterSpacing: 1,
                                    fontFamily: 'Roboto',
                                    fontWeight: FontWeight.w600,
                                    color: secondaryColor),
                                textAlign: TextAlign.center,
                              ),
                              Text(
                                'Grand Total',
                                style: TextStyle(
                                    fontSize: 15,
                                    fontFamily: 'Roboto',
                                    fontWeight: FontWeight.w500,
                                    color: secondaryColor),
                                textAlign: TextAlign.center,
                              ),
                            ],
                          ),
                        )
                      ],
                    )),
              ),
            ),
            Padding(
              padding:
                  const EdgeInsets.only(left: 18, right: 18, bottom: 5, top: 5),
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(Radius.circular(16)),
                  color: Color.fromRGBO(255, 255, 255, 1),
                ),
                child: Padding(
                    padding: const EdgeInsets.all(18.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "Fee Structure",
                          style: TextStyle(
                              fontSize: 20,
                              letterSpacing: 1,
                              fontFamily: 'Roboto',
                              fontWeight: FontWeight.w700,
                              color: Cprimary),
                        ),
                        Divider(
                          thickness: 1,
                          color: grey2,
                        ),
                        LongArrow(year: "1st Year", fees: Firstyearfees),
                        longarrow1(year: "2nd Year", fees: Secondyearfees),
                        longarrow2(year: "3rd Year", fees: Thirdyearfees),
                        longarrow3(year: "4th Year", fees: Fourthyearfees),
                        longarrow4(year: "5th Year", fees: Fifthyearfees),
                        Padding(
                          padding: const EdgeInsets.all(18.0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.end,
                            children: [
                              Text(
                                "Grand Total",
                                style: TextStyle(
                                    fontSize: 14, fontWeight: FontWeight.w600),
                              ),
                              hGap(25),
                              Text(
                                "\$${widget.grandtotal}",
                                style: TextStyle(
                                    fontSize: 14, fontWeight: FontWeight.w600),
                              )
                            ],
                          ),
                        )
                      ],
                    )),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(13.0),
              child: Container(
                padding: EdgeInsets.all(20),
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(15), color: White),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Curriculum",
                      style: TextStyle(
                          fontSize: 20,
                          letterSpacing: 1,
                          fontFamily: 'Roboto',
                          fontWeight: FontWeight.w700,
                          color: Cprimary),
                    ),
                    Divider(
                      thickness: 1,
                      color: grey2,
                    ),
                    Padding(
                      padding: const EdgeInsets.symmetric(
                        vertical: 8.0,
                        horizontal: 10.0,
                      ),
                      child: Column(
                        children: [
                          StreamBuilder(
                            stream: onUpdateActiveIndex,
                            builder: (context, snapShot) {
                              if (widget.Firstyearsubjects.isEmpty) {
                                return Text(
                                    'No subjects available for 1st year');
                              }

                              return ExpansionTile(
                                title: Text(
                                  "1st Year",
                                  style: TextStyle(
                                    fontSize: 18.0,
                                    fontFamily: 'Roboto',
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                children:
                                    widget.Firstyearsubjects.map((subject) {
                                  return Column(
                                    children: [
                                      Divider(
                                        color: titlecolor,
                                      ),
                                      SubjectNames(subject: subject),
                                      SizedBox(
                                          height:
                                              8), // Adjust the height as needed
                                    ],
                                  );
                                }).toList(),
                              );
                            },
                          ),
                          StreamBuilder(
                            stream: onUpdateActiveIndex,
                            builder: (context, snapShot) {
                              if (widget.Firstyearsubjects.isEmpty) {
                                return Text(
                                    'No subjects available for 2nd year');
                              }

                              return ExpansionTile(
                                title: Text(
                                  "2nd Year",
                                  style: TextStyle(
                                    fontSize: 18.0,
                                    fontFamily: 'Roboto',
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                children:
                                    widget.Secondyearsubjects.map((subject) {
                                  return Column(
                                    children: [
                                      Divider(
                                        color: titlecolor,
                                      ),
                                      SubjectNames(subject: subject),
                                      SizedBox(
                                          height:
                                              8), // Adjust the height as needed
                                    ],
                                  );
                                }).toList(),
                              );
                            },
                          ),
                          StreamBuilder(
                            stream: onUpdateActiveIndex,
                            builder: (context, snapShot) {
                              if (widget.Secondyearsubjects.isEmpty) {
                                return Text(
                                    'No subjects available for 3rd year');
                              }

                              return ExpansionTile(
                                title: Text(
                                  "3rd Year",
                                  style: TextStyle(
                                    fontSize: 18.0,
                                    fontFamily: 'Roboto',
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                children:
                                    widget.Secondyearsubjects.map((subject) {
                                  return Column(
                                    children: [
                                      Divider(
                                        color: titlecolor,
                                      ),
                                      SubjectNames(subject: subject),
                                      SizedBox(
                                          height:
                                              8), // Adjust the height as needed
                                    ],
                                  );
                                }).toList(),
                              );
                            },
                          ),
                          StreamBuilder(
                            stream: onUpdateActiveIndex,
                            builder: (context, snapShot) {
                              if (widget.Thirdyearsubjects.isEmpty) {
                                return Text(
                                    'No subjects available for 1st year');
                              }

                              return ExpansionTile(
                                title: Text(
                                  "4th Year",
                                  style: TextStyle(
                                    fontSize: 18.0,
                                    fontFamily: 'Roboto',
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                children:
                                    widget.Thirdyearsubjects.map((subject) {
                                  return Column(
                                    children: [
                                      Divider(
                                        color: titlecolor,
                                      ),
                                      SubjectNames(subject: subject),
                                      SizedBox(
                                          height:
                                              8), // Adjust the height as needed
                                    ],
                                  );
                                }).toList(),
                              );
                            },
                          ),
                          StreamBuilder(
                            stream: onUpdateActiveIndex,
                            builder: (context, snapShot) {
                              if (widget.Fourthyearsubjects.isEmpty) {
                                return Text(
                                    'No subjects available for 1st year');
                              }

                              return ExpansionTile(
                                title: Text(
                                  "5th Year",
                                  style: TextStyle(
                                    fontSize: 18.0,
                                    fontFamily: 'Roboto',
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                children:
                                    widget.Fourthyearsubjects.map((subject) {
                                  return Column(
                                    children: [
                                      Divider(
                                        color: titlecolor,
                                      ),
                                      SubjectNames(subject: subject),
                                      SizedBox(
                                          height:
                                              8), // Adjust the height as needed
                                    ],
                                  );
                                }).toList(),
                              );
                            },
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
            Padding(
              padding:
                  const EdgeInsets.only(left: 18, right: 18, bottom: 5, top: 5),
              child: Container(
                padding: EdgeInsets.all(20),
                decoration: BoxDecoration(
                    color: White, borderRadius: BorderRadius.circular(10)),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Eligibility",
                      style: TextStyle(
                          fontSize: 20,
                          letterSpacing: 1,
                          fontFamily: 'Roboto',
                          fontWeight: FontWeight.w700,
                          color: Cprimary),
                    ),
                    Divider(
                      thickness: 1,
                      color: grey2,
                    ),
                    Padding(
                      padding: const EdgeInsets.only(
                          left: 18.0, top: 10, bottom: 10, right: 18),
                      child: Row(
                        children: [
                          Icon(
                            neetEligibility == "Yes"
                                ? Icons.check_circle_outline
                                : Icons.cancel_outlined,
                            color: Cprimary,
                          ),
                          hGap(15),
                          Text("NEET",
                              style: TextStyle(
                                  fontSize: 16,
                                  fontFamily: 'Roboto',
                                  fontWeight: FontWeight.w500,
                                  color: text5))
                        ],
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.only(
                          left: 18, right: 18, bottom: 5, top: 5),
                      child: Row(
                        children: [
                          Icon(
                            ieltsEligibility == "Yes"
                                ? Icons.check_circle_outline
                                : Icons.cancel_outlined,
                            color: Cprimary,
                          ),
                          hGap(15),
                          Text("IELTS",
                              style: TextStyle(
                                  fontFamily: 'Roboto',
                                  fontSize: 16,
                                  fontWeight: FontWeight.w500,
                                  color: text5))
                        ],
                      ),
                    )
                  ],
                ),
              ),
            ),
            Padding(
              padding:
                  const EdgeInsets.only(left: 18, right: 18, bottom: 5, top: 5),
              child: Container(
                padding: EdgeInsets.all(20),
                decoration: BoxDecoration(
                    color: White, borderRadius: BorderRadius.circular(10)),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Required Documents",
                      style: TextStyle(
                          fontSize: 20,
                          fontFamily: 'Roboto',
                          letterSpacing: 1,
                          fontWeight: FontWeight.w700,
                          color: Cprimary),
                    ),
                    Divider(
                      thickness: 1,
                      color: text5,
                    ),
                    Padding(
                      padding: const EdgeInsets.only(
                          left: 18.0, top: 10, bottom: 10, right: 18),
                      child: Row(
                        children: [
                          Icon(
                            passport
                                ? Icons.check_circle_outline
                                : Icons.cancel_outlined,
                            color: Cprimary,
                          ),
                          hGap(15),
                          Text("Passport",
                              style: TextStyle(
                                  fontFamily: 'Roboto',
                                  fontSize: 16,
                                  fontWeight: FontWeight.w500,
                                  color: text5))
                        ],
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.only(
                          left: 18.0, top: 10, bottom: 10, right: 18),
                      child: Row(
                        children: [
                          Icon(
                            ielts
                                ? Icons.check_circle_outline
                                : Icons.cancel_outlined,
                            color: Cprimary,
                          ),
                          hGap(15),
                          Text("IELTS",
                              style: TextStyle(
                                  fontFamily: 'Roboto',
                                  fontSize: 16,
                                  fontWeight: FontWeight.w500,
                                  color: text5))
                        ],
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.only(
                          left: 18.0, top: 10, bottom: 10, right: 18),
                      child: Row(
                        children: [
                          Icon(
                            tenthCard
                                ? Icons.check_circle_outline
                                : Icons.cancel_outlined,
                            color: Cprimary,
                          ),
                          hGap(15),
                          Text("10Th Cart",
                              style: TextStyle(
                                  fontSize: 16,
                                  fontFamily: 'Roboto',
                                  fontWeight: FontWeight.w500,
                                  color: text5))
                        ],
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.only(
                          left: 18.0, top: 10, bottom: 10, right: 18),
                      child: Row(
                        children: [
                          Icon(
                            twelfthCard
                                ? Icons.check_circle_outline
                                : Icons.cancel_outlined,
                            color: Cprimary,
                          ),
                          hGap(15),
                          Text("12Th Cart",
                              style: TextStyle(
                                  fontSize: 16,
                                  fontFamily: 'Roboto',
                                  fontWeight: FontWeight.w500,
                                  color: text5))
                        ],
                      ),
                    ),
                    Padding(
                      padding:
                          const EdgeInsets.only(left: 18.0, top: 10, right: 18),
                      child: Row(
                        children: [
                          Icon(
                            visa
                                ? Icons.check_circle_outline
                                : Icons.cancel_outlined,
                            color: Cprimary,
                          ),
                          hGap(15),
                          Text("Visa",
                              style: TextStyle(
                                  fontSize: 16,
                                  fontFamily: 'Roboto',
                                  fontWeight: FontWeight.w500,
                                  color: text5))
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.only(
                  left: 18, right: 18, bottom: 15, top: 5),
              child: LongButton(
                text: 'Apply Now',
                action: () {
                  // Navigator.of(context).push(MaterialPageRoute(
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class SubjectNames extends StatelessWidget {
  final String subject;
  const SubjectNames({
    super.key,
    required this.subject,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: EdgeInsets.only(left: 25.0, top: 10, bottom: 10, right: 18),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Icon(
                    Icons.circle,
                    size: 6, // Adjust the size of the dot as needed
                    color:
                        Colors.black, // Adjust the color of the dot as needed
                  ),
                  SizedBox(
                    width: 4,
                  ),
                  Text(
                    subject,
                    style: TextStyle(
                        fontSize: 16,
                        color: text5,
                        fontFamily: 'Roboto',
                        fontWeight: FontWeight.w500),
                  ),
                ],
              ),
            ],
          ),
        ),
      ],
    );
  }
}

void displayModalBottomSheet(context, int id) {
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
      return Padding(
        padding: EdgeInsets.only(
          bottom: MediaQuery.of(context).viewInsets.bottom,
        ),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.only(
              topLeft: Radius.circular(30),
              topRight: Radius.circular(30),
            ),
            color: whiteColor,
          ),
          height: getHeight(context) / 2,
          child: Column(
            children: [
              DropDownDemo(
                universityId: id,
                universityName:
                    "University", // You can pass actual university name if available
              ),
            ],
          ),
        ),
      );
    },
  );
}
