import 'package:flutter/material.dart';
import '../../utils/colors/colors.dart';
import '../../utils/responsive.dart';
import '../../widgets/long_button.dart';

class CustomStepper extends StatefulWidget {
  const CustomStepper({super.key});

  @override
  State<CustomStepper> createState() => _CustomStepperState();
}

class _CustomStepperState extends State<CustomStepper> {
  int _currentIndex = 0;
  final PageController _pageController = PageController();

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  // Widget customDivider(){
  //   return Container(
  //     margin: EdgeInsets.symmetric(horizontal: 2),
  //     height: 10,
  //     width: 2,
  //     decoration: BoxDecoration(
  //         color: primaryColor,
  //         borderRadius: BorderRadius.circular(.25)
  //     ),
  //   );
  // }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.only(top: 20, left: 30, right: 30),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(height: 20),
              Column(
                children: [
                  StepperComponent(
                    currentIndex: _currentIndex,
                    index: 0,
                    onTap: () {
                      setState(() {
                        _currentIndex = 0;
                      });
                      _pageController.jumpToPage(0);
                    },
                  ),
                  // customDivider(),
                  vGap(40),
                  StepperComponent(
                    currentIndex: _currentIndex,
                    index: 1,
                    onTap: () {
                      setState(() {
                        _currentIndex = 1;
                      });
                      _pageController.jumpToPage(1);
                    },
                  ),
                  vGap(40),
                  StepperComponent(
                    currentIndex: _currentIndex,
                    index: 2,
                    onTap: () {
                      setState(() {
                        _currentIndex = 2;
                      });
                      _pageController.jumpToPage(2);
                    },
                  ),
                  vGap(40),
                  StepperComponent(
                    currentIndex: _currentIndex,
                    index: 3,
                    isLast: false,
                    onTap: () {
                      setState(() {
                        _currentIndex = 3;
                      });
                      _pageController.jumpToPage(3);
                    },
                  ),
                  vGap(40),
                  StepperComponent(
                    currentIndex: _currentIndex,
                    index: 4,
                    isLast: false,
                    onTap: () {
                      setState(() {
                        _currentIndex = 4;
                      });
                      _pageController.jumpToPage(4);
                    },
                  ),
                  vGap(40),
                  StepperComponent(
                    currentIndex: _currentIndex,
                    index: 5,
                    isLast: false,
                    onTap: () {
                      setState(() {
                        _currentIndex = 5;
                      });
                      _pageController.jumpToPage(5);
                    },
                  ),
                ],
              ),
              vGap(55),
              LongButton(action: () {}, text: 'Apply Now'),
            ],
          ),
        ),
      ),
    );
  }
}

class StepperComponent extends StatelessWidget {
  int index;
  int currentIndex;
  VoidCallback onTap;
  bool isLast;

  StepperComponent({
    super.key,
    required this.currentIndex,
    required this.index,
    required this.onTap,
    this.isLast = false,
  });

  @override
  Widget build(BuildContext context) {
    return isLast
        ? Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              GestureDetector(
                onTap: onTap,
                child: Container(
                  // width: 0,
                  // height: 0,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(100),
                    color:
                        index == currentIndex ? Colors.red : Colors.transparent,
                    border: Border.all(
                        color: currentIndex >= index
                            ? Colors.red
                            : Colors.black12),
                  ),
                ),
              ),
              // Text('Stage ${index + 1}'),
            ],
          )
        : Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              GestureDetector(
                onTap: onTap,
                child: Row(
                  children: [
                    Container(
                      width: 15,
                      height: 15,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(100),
                        color: index == currentIndex
                            ? primaryColor
                            : Colors.transparent,
                        border: Border.all(
                            color: currentIndex >= index
                                ? primaryColor
                                : Colors.black12),
                      ),
                    ),
                    hGap(30),
                    Text(
                      'Stage ${index + 1}',
                      style: TextStyle(
                          fontSize: 15,
                          fontFamily: 'Roboto',
                          letterSpacing: 2,
                          color: Colors.black,
                          fontWeight: FontWeight.w600),
                    ),
                  ],
                ),
              ),
            ],
          );
  }
}
