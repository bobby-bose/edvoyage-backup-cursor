import 'package:flutter/cupertino.dart';

class longarrow1 extends StatelessWidget {
  final String year;
  final String fees;
  const longarrow1({super.key, required this.year, required this.fees});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(18.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            year,
            style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
          ),
          Image.asset("assets/Vector 61.png"),
          // ClipRect(
          //   child: CustomPaint(
          //     size: Size(MediaQuery.of(context).size.width, 700),
          //     painter: ArrowPainter(),
          //   ),
          // ),
          Text(
            fees,
            style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
          )
        ],
      ),
    );
  }
}
