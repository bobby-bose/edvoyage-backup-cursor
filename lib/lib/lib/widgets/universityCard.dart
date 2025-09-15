import 'package:flutter/material.dart';
import 'package:notes/utils/colors/colors.dart';

class UniversityCard extends StatelessWidget {
  late String image;
  late String title;
  late String subTitle;
  late String text1;
  late String text1_2;
  late String text2;
  late String text2_2;
  late String text3;
  late String text3_2;
  late String text4;
  late String text4_2;
  late Function() action;
  var styling = {};

  UniversityCard({
    super.key,
    required this.image,
    required this.title,
    required this.subTitle,
    required this.text1,
    required this.text1_2,
    required this.text2,
    required this.text2_2,
    required this.text3,
    required this.text3_2,
    required this.text4,
    required this.text4_2,
    required this.action,
    required this.styling,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(10),
      width: 327,
      height: 161,
      decoration: BoxDecoration(
        color: thirdColor,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        children: [
          ListTile(
            leading: Image.asset(image),
            title: Text(
              title,
              textScaleFactor: 1,
              style: TextStyle(
                fontFamily: 'Roboto',
                color: primaryColor,
                fontWeight: FontWeight.bold,
              ),
            ),
            subtitle: Text(
              subTitle,
              textScaleFactor: .8,
              style: TextStyle(
                fontFamily: 'Roboto',
                color: grey2,
                fontWeight: FontWeight.bold,
              ),
            ),
            trailing: Container(
              margin: EdgeInsets.only(bottom: 25),
              child: Image.asset('assets/external.png'),
            ),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              Column(
                children: [
                  Text(
                    text1,
                    textScaleFactor: .9,
                    style: TextStyle(
                      fontFamily: 'Roboto',
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    text1_2,
                    textScaleFactor: .8,
                    style: TextStyle(
                      fontFamily: 'Roboto',
                      fontWeight: FontWeight.w500,
                      color: grey2,
                    ),
                  ),
                ],
              ),
              Column(
                children: [
                  Text(
                    text2,
                    textScaleFactor: .9,
                    style: TextStyle(
                      fontFamily: 'Roboto',
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    text2_2,
                    textScaleFactor: .8,
                    style: TextStyle(
                      fontFamily: 'Roboto',
                      fontWeight: FontWeight.w500,
                      color: grey2,
                    ),
                  ),
                ],
              ),
              Column(
                children: [
                  Text(
                    text3,
                    textScaleFactor: .9,
                    style: TextStyle(
                      fontFamily: 'Roboto',
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    text3_2,
                    textScaleFactor: .8,
                    style: TextStyle(
                      fontFamily: 'Roboto',
                      fontWeight: FontWeight.w500,
                      color: grey2,
                    ),
                  ),
                ],
              ),
              Column(
                children: [
                  Text(
                    text4,
                    textScaleFactor: .9,
                    style: TextStyle(
                      fontFamily: 'Roboto',
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    text4_2,
                    textScaleFactor: .8,
                    style: TextStyle(
                      fontFamily: 'Roboto',
                      fontWeight: FontWeight.w500,
                      color: grey2,
                    ),
                  ),
                ],
              ),
            ],
          ),
          Spacer(),
          SizedBox(
            width: 158,
            height: 30,
            child: TextButton(
              style: ButtonStyle(
                backgroundColor: WidgetStateProperty.all(
                  styling["backgroundcolor"],
                ),
                shape: WidgetStateProperty.all(
                  StadiumBorder(side: BorderSide(color: styling["border"])),
                ),
              ),
              onPressed: action,
              child: Text(
                'Shortlist',
                style: TextStyle(
                  fontFamily: 'Roboto',
                  color: styling["textcolor"],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class CountryButton extends StatelessWidget {
  late String text;
  late Color buttonColor;
  late Color textColor;

  CountryButton({
    super.key,
    required this.text,
    required this.buttonColor,
    required this.textColor,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 31,
      width: 59,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.all(Radius.circular(7.5)),
        color: buttonColor,
      ),
      child: TextButton(
        onPressed: () {},
        child: Text(
          text,
          style: TextStyle(fontFamily: 'Roboto', color: textColor),
        ),
      ),
    );
  }
}
