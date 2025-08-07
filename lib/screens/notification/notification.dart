import 'dart:convert';
import 'package:flutter/material.dart';
import 'dart:math' as math;
import 'package:http/http.dart' as http;
import '../../_env/env.dart';
import '../../models/all_notification.dart';
import '../../utils/colors/colors.dart';
import '../../utils/responsive.dart';
import '../../models/notification_offer.dart';
import '../home_screen/homeScreen.dart';

class NotificationScreen extends StatefulWidget {
  const NotificationScreen({super.key});

  @override
  _NotificationScreenState createState() => _NotificationScreenState();
}

class _NotificationScreenState extends State<NotificationScreen>
    with SingleTickerProviderStateMixin {
  TabController? _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    super.dispose();
    _tabController!.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        // back icon
        leading: IconButton(
          onPressed: () {
            // navigate to HomeScreen() i dont want pop

            Navigator.pushReplacement(
              context,
              MaterialPageRoute(
                builder: (context) => HomeScreen(),
              ),
            );
          },
          icon: Icon(
            Icons.arrow_back_ios_outlined,
            color: primaryColor,
          ),
        ),

        elevation: 1,
        title: Text(
          "Notification",
          style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 20,
              color: primaryColor,
              fontWeight: FontWeight.w700),
        ),
        backgroundColor: Colors.white,
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: getWidth(context) / 2,
            child: Padding(
              padding: const EdgeInsets.only(top: 10, bottom: 10),
              child: TabBar(
                unselectedLabelColor: Color.fromARGB(255, 54, 53, 53),
                indicatorSize: TabBarIndicatorSize.label,
                indicator: BoxDecoration(
                    borderRadius: BorderRadius.circular(50), color: Cprimary),
                labelColor: Colors.white,
                controller: _tabController,
                indicatorColor: Cprimary,
                tabs: [
                  Tab(
                    height: MediaQuery.of(context).size.height *
                        0.03, // Adjust the multiplier as needed
                    child: Container(
                      padding: EdgeInsets.symmetric(
                        horizontal: MediaQuery.of(context).size.width *
                            0.02, // Adjust the multiplier as needed
                      ),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(50),
                        border: Border.all(
                          color: Color.fromARGB(255, 215, 200, 200),
                          width: 1,
                        ),
                      ),
                      child: Align(
                        alignment: Alignment.center,
                        child: Text(
                          "Offers",
                          style: TextStyle(
                            fontFamily: 'Poppins',
                            fontWeight: FontWeight.w500,
                            letterSpacing: 1,
                          ),
                        ),
                      ),
                    ),
                  ),
                  Tab(
                    height: MediaQuery.of(context).size.height *
                        0.03, // Adjust the multiplier as needed
                    child: Container(
                      padding: EdgeInsets.symmetric(
                        horizontal: MediaQuery.of(context).size.width *
                            0.02, // Adjust the multiplier as needed
                      ),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(50),
                        border: Border.all(
                          color: Color.fromARGB(255, 215, 200, 200),
                          width: 1,
                        ),
                      ),
                      child: Align(
                        alignment: Alignment.center,
                        child: Text(
                          "All",
                          style: TextStyle(
                            fontFamily: 'Poppins',
                            fontWeight: FontWeight.w500,
                            letterSpacing: 1,
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          Divider(
            thickness: 2,
          ),
          Expanded(
            child: TabBarView(
              controller: _tabController,
              children: [
                AllNotifications(),
                Offers(),
              ],
            ),
          )
        ],
      ),
    );
  }
}

class AllNotifications extends StatefulWidget {
  const AllNotifications({super.key});

  @override
  State<AllNotifications> createState() => _AllNotificationsState();
}

class _AllNotificationsState extends State<AllNotifications> {
  Future<NotificationAll> getallnotifications() async {
    try {
      final response = await http.get(Uri.parse(BaseUrl.getallnotifications));
      print(response.body[0]);
      if (response.statusCode == 200) {
        return NotificationAll.fromJson(jsonDecode(response.body));
      } else {
        throw Exception('Failed to load notifications');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(8.0),
      child: FutureBuilder<NotificationAll>(
        future: getallnotifications(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(
              child: CircularProgressIndicator(
                color: Cprimary,
                backgroundColor: secondaryColor,
              ),
            );
          } else if (snapshot.hasError) {
            return Center(
              child: Text('Error: ${snapshot.error}'),
            );
          } else if (!snapshot.hasData || snapshot.data!.data.isEmpty) {
            return Center(
              child: Text('No notifications available.'),
            );
          } else {
            final filteredData = snapshot.data!.data
                .where((d) => d.notification_type == 'ALL')
                .toList();

            return ListView.builder(
              itemCount: filteredData.length,
              itemBuilder: (context, index) {
                return Column(
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Column(
                            children: [
                              CircleAvatar(
                                radius: 19,
                                backgroundColor: contr3,
                                child: CircleAvatar(
                                  radius: 15,
                                  backgroundColor: VIPtext,
                                  child: Transform.rotate(
                                    angle: 180 * math.pi / 150,
                                    child: Icon(
                                      Icons.label_outlined,
                                      size: 20,
                                    ),
                                  ),
                                ),
                              )
                            ],
                          ),
                          hGap(20),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  filteredData[index].content,
                                  style: TextStyle(
                                    fontFamily: 'Poppins',
                                    fontSize: 14,
                                  ),
                                ),
                                vGap(5),
                                Text(
                                  "10 Hours Ago",
                                  style: TextStyle(
                                    fontFamily: 'Poppins',
                                    fontSize: 12,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    Divider(
                      thickness: 2,
                    ),
                  ],
                );
              },
            );
          }
        },
      ),
    );
  }
}

class Offers extends StatefulWidget {
  const Offers({super.key});

  @override
  State<Offers> createState() => _OffersState();
}

class _OffersState extends State<Offers> {
  Future<NotificationOffer> getnotificationofferApi() async {
    try {
      final response = await http.get(Uri.parse(BaseUrl.getallnotifications));
      if (response.statusCode == 200) {
        return NotificationOffer.fromJson(jsonDecode(response.body));
      } else {
        throw Exception('Failed to load notification offers');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(8.0),
      child: FutureBuilder<NotificationOffer>(
        future: getnotificationofferApi(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(
              child: CircularProgressIndicator(
                color: Cprimary,
                backgroundColor: secondaryColor,
              ),
            );
          } else if (snapshot.hasError) {
            return Center(
              child: Text('Error: ${snapshot.error}'),
            );
          } else if (!snapshot.hasData || snapshot.data!.data.isEmpty) {
            return Center(
              child: Text('No notification offers available.'),
            );
          } else {
            return ListView.builder(
              itemCount: snapshot.data!.data.length,
              itemBuilder: (context, index) {
                return Column(
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Column(
                            children: [
                              CircleAvatar(
                                radius: 19,
                                backgroundColor: contr3,
                                child: CircleAvatar(
                                  radius: 15,
                                  backgroundColor: VIPtext,
                                  child: Transform.rotate(
                                    angle: 180 * math.pi / 150,
                                    child: Icon(
                                      Icons.label_outlined,
                                      size: 20,
                                    ),
                                  ),
                                ),
                              )
                            ],
                          ),
                          hGap(20),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  snapshot.data!.data[index].content,
                                  style: TextStyle(
                                    fontFamily: 'Poppins',
                                    fontSize: 14,
                                  ),
                                ),
                                vGap(5),
                                Text(
                                  "10 Hours Ago",
                                  style: TextStyle(
                                    fontFamily: 'Poppins',
                                    fontSize: 12,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    Divider(
                      thickness: 2,
                    ),
                  ],
                );
              },
            );
          }
        },
      ),
    );
  }
}
