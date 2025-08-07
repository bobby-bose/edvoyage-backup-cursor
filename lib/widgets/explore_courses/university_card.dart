import 'package:flutter/material.dart';

class UniversityCard extends StatelessWidget {
  final String image;
  final String title;
  final String subTitle;
  final String estd;
  final double dvRank;
  final dynamic Function() action;

  const UniversityCard({
    super.key,
    required this.image,
    required this.title,
    required this.subTitle,
    required this.estd,
    required this.dvRank,
    required this.action,
  });

  @override
  Widget build(BuildContext context) {
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
                      Image.asset(
                        image,
                      ),
                    ],
                  ),
                  Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: TextStyle(
                          fontSize: 15,
                          fontFamily: 'Roboto',
                          color: Colors.blue, // Change to your color
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      SizedBox(height: 4),
                      Text(
                        subTitle,
                        style: TextStyle(
                          fontFamily: 'Roboto',
                          fontSize: 12,
                          color: Colors.grey, // Change to your color
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      SizedBox(height: 15),
                      Row(
                        children: [
                          Text(
                            "ESTD : ",
                            style: TextStyle(
                              fontFamily: 'Roboto',
                              fontSize: 12,
                              color: Colors.grey, // Change to your color
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          Text(
                            estd,
                            style: TextStyle(
                              fontFamily: 'Roboto',
                              fontSize: 12,
                              color: Colors.grey, // Change to your color
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                      SizedBox(height: 3),
                      Row(
                        children: [
                          Text(
                            "DV Rank",
                            style: TextStyle(
                              fontFamily: 'Roboto',
                              fontSize: 12,
                              color: Colors.grey, // Change to your color
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          SizedBox(
                            width: 3,
                          ),
                          // Assuming dvRank is a double value
                          Text(
                            dvRank.toString(),
                            style: TextStyle(
                              fontFamily: 'Roboto',
                              fontSize: 12,
                              color: Colors.grey, // Change to your color
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ],
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  IconButton(
                    onPressed: action,
                    icon: Icon(
                      Icons.bookmark_outline_sharp,
                      color: Colors.grey,
                      size: 30,
                    ),
                  ),
                  Container(
                    height: 40, // Set the desired height
                    width: 100, // Set the desired width
                    decoration: BoxDecoration(
                      color: Colors.blue, // Change to your color
                      borderRadius: BorderRadius.circular(5),
                    ),
                    child: TextButton(
                      onPressed: action,
                      child: const Text(
                        'View',
                        style: TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.w600,
                          fontFamily: 'Roboto',
                          color: Colors.white,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
