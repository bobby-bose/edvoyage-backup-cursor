// import 'dart:convert';
// import 'package:flutter/material.dart';
// import 'package:http/http.dart' as http;
// import '../../models/mcq.dart';
// import '../../utils/avatar.dart';
// import '../../utils/colors/colors.dart';
// import '../../utils/responsive.dart';
// import '../../widgets/long_button.dart';
// import '../exploreUniversity_screen/exploreCoursesTab.dart';
// import '../notification/notification.dart';

// class Sad extends StatefulWidget {
//   const Sad({Key? key}) : super(key: key);

//   @override
//   State<Sad> createState() => _SadState();
// }

// class _SadState extends State<Sad> {
//   Measurements? size;
//   var selectedIndex;

//   Future<MCQ> getMCQApi() async {
//     var response = await http.get(
//       Uri.parse(
//         'https://edvoge.com/api/v1/mcq/get',
//       ),
//     );
//     print(response.body);
//     if (response.statusCode == 200) {
//       var jsonResponse = json.decode(response.body);
//       return MCQ.fromJson(jsonResponse);
//     } else {
//       throw Exception('Failed to load jobs from API');
//     }
//   }

//   @override
//   Widget build(BuildContext context) {
//     size = Measurements(MediaQuery.of(context).size);
//     return Scaffold(
//       backgroundColor: vBarBgcolor,
//       appBar: AppBar(
//         backgroundColor: Colors.white,
//         elevation: 0.2,
//         automaticallyImplyLeading: false,
//         centerTitle: true,
//         title: Container(
//           height: 250, // Set the width of the container
//           height: 200, // Set the height of the container
//           child:
//               Image.asset(edvoyagelogo1), // Replace with the actual image path
//         ),
//         actions: [
//           IconButton(
//               icon: Icon(
//                 Icons.notifications,
//                 color: primaryColor,
//               ),
//               onPressed: () {
//                 Navigator.push(
//                     context,
//                     MaterialPageRoute(
//                         builder: (context) => NotificationScreen()));
//               })
//         ],
//       ),
//       body: Padding(
//         padding: const EdgeInsets.all(8.0),
//         child: Column(
//           children: [
//             Center(
//               child: Container(
//                 alignment: Alignment.center,
//                 height: size?.hp(6),
//                 width: size?.wp(95),
//                 decoration: BoxDecoration(
//                     color: Color.fromRGBO(192, 235, 231, 1),
//                     borderRadius: BorderRadius.circular(25)),
//                 child: Text(
//                   '\"It\'s alright, it\'s okay\"',
//                   textScaleFactor: 1.2,
//                   style: TextStyle(
//                       color: primaryColor, fontWeight: FontWeight.bold),
//                 ),
//               ),
//             ),
//             Center(
//               child: Container(
//                 margin: EdgeInsets.symmetric(vertical: 10),
//                 height: size?.hp(30),
//                 width: size?.wp(95),
//                 decoration: BoxDecoration(
//                     color: thirdColor,
//                     borderRadius: BorderRadius.circular(10),
//                     boxShadow: [
//                       BoxShadow(
//                           offset: Offset(1, 1),
//                           blurRadius: 2,
//                           color: grey2,
//                           spreadRadius: 2)
//                     ]),
//                 child: Column(
//                   mainAxisAlignment: MainAxisAlignment.spaceEvenly,
//                   children: [
//                     Text(
//                       'Explore Courses & Universities',
//                       textScaleFactor: 1.8,
//                       style: TextStyle(
//                         color: primaryColor,
//                         fontWeight: FontWeight.w800,
//                       ),
//                     ),
//                     Row(
//                       mainAxisAlignment: MainAxisAlignment.spaceEvenly,
//                       children: [
//                         Container(
//                           height: size?.hp(14),
//                           width: size?.wp(42),
//                           decoration: BoxDecoration(
//                               color: thirdColor,
//                               borderRadius: BorderRadius.circular(10),
//                               boxShadow: [
//                                 BoxShadow(
//                                     offset: Offset(0, 0),
//                                     spreadRadius: 1,
//                                     color: grey2)
//                               ]),
//                           child: Column(
//                             mainAxisAlignment: MainAxisAlignment.center,
//                             children: [
//                               Container(
//                                 height: size?.hp(4.5),
//                                 width: size?.wp(9.6),
//                                 child: Image.asset(
//                                   universityimage,
//                                 ),
//                               ),
//                               Text(
//                                 '300+',
//                                 textScaleFactor: 1.5,
//                                 style: TextStyle(
//                                   fontWeight: FontWeight.w900,
//                                 ),
//                               ),
//                               Text(
//                                 'Universiteis',
//                                 style: TextStyle(
//                                   fontWeight: FontWeight.w800,
//                                 ),
//                               )
//                             ],
//                           ),
//                         ),
//                         Container(
//                           height: size?.hp(14),
//                           width: size?.wp(42),
//                           decoration: BoxDecoration(
//                               color: thirdColor,
//                               borderRadius: BorderRadius.circular(10),
//                               boxShadow: [
//                                 BoxShadow(
//                                     offset: Offset(0, 0),
//                                     spreadRadius: 1,
//                                     color: grey2)
//                               ]),
//                           child: Column(
//                             mainAxisAlignment: MainAxisAlignment.center,
//                             children: [
//                               Container(
//                                 height: size?.hp(4.5),
//                                 width: size?.wp(9.6),
//                                 child: Image.asset(
//                                   coursesimage,
//                                 ),
//                               ),
//                               Text(
//                                 '30,000+',
//                                 textScaleFactor: 1.5,
//                                 style: TextStyle(
//                                   fontWeight: FontWeight.w900,
//                                 ),
//                               ),
//                               Text(
//                                 'Courses',
//                                 style: TextStyle(
//                                   fontWeight: FontWeight.w800,
//                                 ),
//                               )
//                             ],
//                           ),
//                         )
//                       ],
//                     ),
//                     LongButton(
//                         action: () {
//                           Navigator.push(
//                               context,
//                               MaterialPageRoute(
//                                   builder: (context) => ExploreCourses()));
//                         },
//                         text: 'Explore Now'),
//                   ],
//                 ),
//               ),
//             ),
//             Expanded(
//                 child: FutureBuilder<MCQ>(
//                     future: getMCQApi(),
//                     builder: (context, snapshot) {
//                       if (snapshot.hasData) {
//                         return ListView.builder(

//                             // write based on the MCQ model the code for itemcount

//                             itemCount: 0,
//                             itemBuilder: (context, index) {
//                               return Padding(
//                                   padding: const EdgeInsets.only(
//                                       left: 18.0,
//                                       right: 18.0,
//                                       top: 8,
//                                       bottom: 8),
//                                   child: Column(children: [
//                                     Container(
//                                         padding: EdgeInsets.all(13),
//                                         decoration: BoxDecoration(
//                                             color: White,
//                                             borderRadius:
//                                                 BorderRadius.circular(10)),
//                                         child: Column(
//                                             crossAxisAlignment:
//                                                 CrossAxisAlignment.start,
//                                             children: [
//                                               Text(
//                                                 "MCQ of the day",
//                                                 style: TextStyle(
//                                                     fontSize: 16,
//                                                     fontFamily: 'Roboto',
//                                                     fontWeight: FontWeight.w800,
//                                                     color: Cprimary),
//                                               ),
//                                               Divider(
//                                                 thickness: 1,
//                                                 color: grey2,
//                                               ),
//                                               Padding(
//                                                 padding:
//                                                     const EdgeInsets.all(8.0),
//                                                 child: Text(
//                                                   snapshot.data!.data[index]
//                                                       .question,
//                                                   style: TextStyle(
//                                                       fontFamily: 'Roboto',
//                                                       fontWeight:
//                                                           FontWeight.w800,
//                                                       fontSize: 19),
//                                                 ),
//                                               ),
//                                               Padding(
//                                                 padding:
//                                                     const EdgeInsets.all(7.0),
//                                                 child: GestureDetector(
//                                                   onTap: () {},
//                                                   child: Container(
//                                                     height:
//                                                         getHeight(context) / 14,
//                                                     decoration: BoxDecoration(
//                                                         borderRadius:
//                                                             BorderRadius.all(
//                                                                 Radius.circular(
//                                                                     10)),
//                                                         border: Border.all(
//                                                             color: grey2)),
//                                                     child: Padding(
//                                                       padding:
//                                                           const EdgeInsets.all(
//                                                               8.0),
//                                                       child: Row(
//                                                         mainAxisAlignment:
//                                                             MainAxisAlignment
//                                                                 .spaceBetween,
//                                                         children: [
//                                                           Expanded(
//                                                               child: RichText(
//                                                             text: TextSpan(
//                                                               children: <TextSpan>[
//                                                                 TextSpan(
//                                                                   text: 'A - ',
//                                                                   style: TextStyle(
//                                                                       fontSize:
//                                                                           15,
//                                                                       color:
//                                                                           darkblack,
//                                                                       fontWeight:
//                                                                           FontWeight
//                                                                               .w700),
//                                                                 ),
//                                                                 TextSpan(
//                                                                   text: snapshot
//                                                                       .data!
//                                                                       .data[
//                                                                           index]
//                                                                       .option_1,
//                                                                   style: TextStyle(
//                                                                       fontSize:
//                                                                           15,
//                                                                       color:
//                                                                           darkblack,
//                                                                       fontWeight:
//                                                                           FontWeight
//                                                                               .w800),
//                                                                 ),
//                                                               ],
//                                                             ),
//                                                           )),
//                                                         ],
//                                                       ),
//                                                     ),
//                                                   ),
//                                                 ),
//                                               ),
//                                               Padding(
//                                                 padding:
//                                                     const EdgeInsets.all(7.0),
//                                                 child: GestureDetector(
//                                                   onTap: () {},
//                                                   child: Container(
//                                                     height:
//                                                         getHeight(context) / 14,
//                                                     decoration: BoxDecoration(
//                                                         borderRadius:
//                                                             BorderRadius.all(
//                                                                 Radius.circular(
//                                                                     10)),
//                                                         border: Border.all(
//                                                             color: grey2)),
//                                                     child: Padding(
//                                                       padding:
//                                                           const EdgeInsets.all(
//                                                               8.0),
//                                                       child: Row(
//                                                         mainAxisAlignment:
//                                                             MainAxisAlignment
//                                                                 .spaceBetween,
//                                                         children: [
//                                                           Expanded(
//                                                               child: RichText(
//                                                             text: TextSpan(
//                                                               children: <TextSpan>[
//                                                                 TextSpan(
//                                                                   text: 'B - ',
//                                                                   style: TextStyle(
//                                                                       fontSize:
//                                                                           15,
//                                                                       color:
//                                                                           darkblack,
//                                                                       fontWeight:
//                                                                           FontWeight
//                                                                               .w800),
//                                                                 ),
//                                                                 TextSpan(
//                                                                   text: snapshot
//                                                                       .data!
//                                                                       .data[
//                                                                           index]
//                                                                       .option_2,
//                                                                   style: TextStyle(
//                                                                       fontSize:
//                                                                           15,
//                                                                       color:
//                                                                           darkblack,
//                                                                       fontWeight:
//                                                                           FontWeight
//                                                                               .w800),
//                                                                 ),
//                                                               ],
//                                                             ),
//                                                           )),
//                                                         ],
//                                                       ),
//                                                     ),
//                                                   ),
//                                                 ),
//                                               ),
//                                               Padding(
//                                                 padding:
//                                                     const EdgeInsets.all(7.0),
//                                                 child: GestureDetector(
//                                                   onTap: () {},
//                                                   child: Container(
//                                                     height:
//                                                         getHeight(context) / 14,
//                                                     decoration: BoxDecoration(
//                                                         borderRadius:
//                                                             BorderRadius.all(
//                                                                 Radius.circular(
//                                                                     10)),
//                                                         border: Border.all(
//                                                             color: grey2)),
//                                                     child: Padding(
//                                                       padding:
//                                                           const EdgeInsets.all(
//                                                               8.0),
//                                                       child: Row(
//                                                         mainAxisAlignment:
//                                                             MainAxisAlignment
//                                                                 .spaceBetween,
//                                                         children: [
//                                                           Expanded(
//                                                               child: RichText(
//                                                             text: TextSpan(
//                                                               children: <TextSpan>[
//                                                                 TextSpan(
//                                                                   text: 'C - ',
//                                                                   style: TextStyle(
//                                                                       fontSize:
//                                                                           15,
//                                                                       color:
//                                                                           darkblack,
//                                                                       fontWeight:
//                                                                           FontWeight
//                                                                               .w800),
//                                                                 ),
//                                                                 TextSpan(
//                                                                   text: snapshot
//                                                                       .data!
//                                                                       .data[
//                                                                           index]
//                                                                       .option_3,
//                                                                   style: TextStyle(
//                                                                       fontSize:
//                                                                           15,
//                                                                       color:
//                                                                           darkblack,
//                                                                       fontWeight:
//                                                                           FontWeight
//                                                                               .w800),
//                                                                 ),
//                                                               ],
//                                                             ),
//                                                           )),
//                                                         ],
//                                                       ),
//                                                     ),
//                                                   ),
//                                                 ),
//                                               ),
//                                               Padding(
//                                                 padding:
//                                                     const EdgeInsets.all(7.0),
//                                                 child: GestureDetector(
//                                                   onTap: () {},
//                                                   child: Container(
//                                                     height:
//                                                         getHeight(context) / 14,
//                                                     decoration: BoxDecoration(
//                                                         borderRadius:
//                                                             BorderRadius.all(
//                                                                 Radius.circular(
//                                                                     10)),
//                                                         border: Border.all(
//                                                             color: grey2)),
//                                                     child: Padding(
//                                                       padding:
//                                                           const EdgeInsets.all(
//                                                               8.0),
//                                                       child: Row(
//                                                         mainAxisAlignment:
//                                                             MainAxisAlignment
//                                                                 .spaceBetween,
//                                                         children: [
//                                                           Expanded(
//                                                             child: RichText(
//                                                               text: TextSpan(
//                                                                 children: <TextSpan>[
//                                                                   TextSpan(
//                                                                     text:
//                                                                         'D - ',
//                                                                     style: TextStyle(
//                                                                         fontSize:
//                                                                             15,
//                                                                         color:
//                                                                             darkblack,
//                                                                         fontWeight:
//                                                                             FontWeight.w800),
//                                                                   ),
//                                                                   TextSpan(
//                                                                     text: snapshot
//                                                                         .data!
//                                                                         .data[
//                                                                             index]
//                                                                         .option_4,
//                                                                     style: TextStyle(
//                                                                         fontSize:
//                                                                             15,
//                                                                         color:
//                                                                             darkblack,
//                                                                         fontWeight:
//                                                                             FontWeight.w800),
//                                                                   ),
//                                                                 ],
//                                                               ),
//                                                             ),
//                                                           ),
//                                                         ],
//                                                       ),
//                                                     ),
//                                                   ),
//                                                 ),
//                                               ),
//                                               Divider(
//                                                 thickness: 1,
//                                                 color: titlecolor,
//                                               ),
//                                               Padding(
//                                                 padding: const EdgeInsets.only(
//                                                     top: 8, bottom: 8),
//                                                 child: Row(
//                                                   mainAxisAlignment:
//                                                       MainAxisAlignment
//                                                           .spaceBetween,
//                                                   children: [
//                                                     InkWell(
//                                                       onTap: () {
//                                                         setState(() {
//                                                           selectedIndex = true;
//                                                         });
//                                                       },
//                                                       child: ImageIcon(
//                                                         AssetImage(
//                                                           "assets/bookmark.png",
//                                                         ),
//                                                         color: (selectedIndex ==
//                                                                 true)
//                                                             ? Cprimary
//                                                             : Color(0xff9A9A9A),
//                                                       ),
//                                                     ),
//                                                   ],
//                                                 ),
//                                               )
//                                             ]))
//                                   ]));
//                             });
//                       } else {
//                         return Center(
//                             child: CircularProgressIndicator(
//                           color: Cprimary,
//                           backgroundColor: secondaryColor,
//                         ));
//                       }
//                     }))
//           ],
//         ),
//       ),
//     );
//   }
// }
