import 'package:flutter/material.dart';

class LongArrow extends StatelessWidget {
  final String year;
  final String fees;
  const LongArrow({super.key, required this.year, required this.fees});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(18.0),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                "1st Year",
                style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
              ),
              Image.asset("assets/Vector 61.png"),
              Text(
                fees,
                style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
              )
            ],
          ),
        ],
      ),
    );
  }
}
