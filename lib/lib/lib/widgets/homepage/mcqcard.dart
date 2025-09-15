import 'package:flutter/material.dart';

Widget buildMCQCard() {
  return Padding(
    padding: EdgeInsets.only(top: 10, left: 5, right: 5, bottom: 10),
    child: Column(
      children: [
        Container(
          padding: EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(10),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                "MCQ of the day",
                style: TextStyle(
                  fontSize: 16,
                  fontFamily: 'Roboto',
                  fontWeight: FontWeight.w800,
                  color: Colors
                      .black, // Replace 'primaryColor' with the desired color
                ),
              ),
              Divider(
                thickness: 1,
                color: Colors.grey,
              ),
              Padding(
                padding: EdgeInsets.all(8.0),
                child: Text(
                  "Which of these is a major difference between oogenesis and spermatogenesis?",
                  style: TextStyle(
                    letterSpacing: 1,
                    fontFamily: 'Roboto',
                    fontWeight: FontWeight.w700,
                    fontSize: 19,
                  ),
                ),
              ),
              buildOption(
                "A",
                "Spermatogenesis leads to two sperm, while oogenesis leads to one egg",
              ),
              buildOption(
                "B",
                "Oogenesis leads to four eggs while spermatogenesis",
              ),
              buildOption(
                "C",
                "Spermatogenesis leads to four sperm, while oogenesis leads to one egg",
              ),
              buildOption(
                "D",
                "Oogenesis leads to two eggs while spermatogenesis leads to one sperm",
              ),
              Divider(
                thickness: 1,
                color: Colors.grey,
              ),
              Padding(
                padding: EdgeInsets.only(top: 8, bottom: 8),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    InkWell(
                      onTap: () {},
                      child: Icon(
                        Icons.bookmark_border,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ],
    ),
  );
}

Widget buildOption(String option, String text) {
  return ListTile(
    leading: Text(option),
    title: Text(text),
  );
}
