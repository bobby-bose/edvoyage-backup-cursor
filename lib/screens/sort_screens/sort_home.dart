import 'package:flutter/material.dart';

import '../FilteredUniversities/FilteredUniversities.dart';
import 'uniquecities.dart';

List uniqueranks = [
  "1",
  "2",
  "3",
  "4",
];

List uniqueratings = [
  "4 & Up",
  "3 & Up",
  "2 & Up",
  "1 & Up",
];

List chooseoptions = [];
int ratingoption = 0;
String cityoption = "";
int rankoption = 0;

// when this page is called every selected option is removed
// also all the checked isons are unchecked

class SortHome extends StatefulWidget {
  const SortHome({super.key});

  @override
  State<SortHome> createState() => _SortHomeState();
}

class _SortHomeState extends State<SortHome> {
  int _selectedIndex = 0;
  Widget CurrentWidget = SortOne();
  bool isSelected1 = false;
  bool isSelected2 = false;
  bool isSelected3 = false;
  bool isSelected4 = false;

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
      if (_selectedIndex == 1) {
        setState(() {
          isSelected1 = true;
          isSelected2 = false;
          isSelected3 = false;
          isSelected4 = false;
          CurrentWidget = SortOne();
        });
      } else if (_selectedIndex == 2) {
        setState(() {
          isSelected2 = true;
          isSelected1 = false;
          isSelected3 = false;
          isSelected4 = false;

          CurrentWidget = SortTwo();
        });
      } else if (_selectedIndex == 3) {
        setState(() {
          isSelected3 = true;
          isSelected1 = false;
          isSelected2 = false;
          isSelected4 = false;

          CurrentWidget = SortThree();
        });
      } else {
        setState(() {
          isSelected1 = true;
          isSelected2 = false;
          isSelected3 = false;
          isSelected4 = false;
          CurrentWidget = SortOne();
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        toolbarHeight: MediaQuery.of(context).size.height * 0.1,
        leading: IconButton(
          icon: Icon(
            Icons.arrow_back,
            color: Color.fromARGB(255, 49, 148, 76),
            size: 25,
          ),
          onPressed: () => Navigator.of(context).pop(),
        ),
        title: Text(
          'Filter',
          style: TextStyle(
            color: Color.fromARGB(255, 49, 148, 76),
            fontSize: 25,
            fontFamily: "Poppins",
            fontWeight: FontWeight.w400,
          ),
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: Row(
              children: [
                Expanded(
                  flex: 4,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      GestureDetector(
                        onTap: () => _onItemTapped(1),
                        child: Container(
                          decoration: BoxDecoration(
                            border: Border(
                              bottom: BorderSide(
                                color: isSelected1
                                    ? Color.fromARGB(255, 64, 62, 62)
                                    : Color.fromARGB(255, 215, 210, 210),
                                width: 2.0,
                              ),
                            ),
                          ),
                          padding: EdgeInsets.symmetric(
                              vertical: 16, horizontal: 24),
                          child: Text(
                            "Rating",
                            style: TextStyle(
                              color: isSelected1
                                  ? Color.fromARGB(255, 64, 62, 62)
                                  : Color.fromARGB(255, 215, 210, 210),
                              fontWeight: FontWeight.bold,
                              fontSize: 20,
                            ),
                          ),
                        ),
                      ),
                      GestureDetector(
                        onTap: () => _onItemTapped(2),
                        child: Container(
                          decoration: BoxDecoration(
                            border: Border(
                              bottom: BorderSide(
                                color: isSelected2
                                    ? Color.fromARGB(255, 64, 62, 62)
                                    : Color.fromARGB(255, 215, 210, 210),
                                width: 2.0,
                              ),
                            ),
                          ),
                          padding: EdgeInsets.symmetric(
                              vertical: 16, horizontal: 24),
                          child: Text(
                            "Cities",
                            style: TextStyle(
                              color: isSelected2
                                  ? Color.fromARGB(255, 64, 62, 62)
                                  : Color.fromARGB(255, 215, 210, 210),
                              fontWeight: FontWeight.bold,
                              fontSize: 20,
                            ),
                          ),
                        ),
                      ),
                      Expanded(child: _buildTabItemEmpty()),
                    ],
                  ),
                ),
                Expanded(
                  flex: 6,
                  child: CurrentWidget,
                ),
              ],
            ),
          ),
          SizedBox(
            width: 10,
          ),
          Row(children: [
            sort_bottom_buttom(
                text: "Close",
                color: Color.fromARGB(255, 9, 12, 10),
                navigation: () {
                  Navigator.of(context).pop();
                }),
            sort_bottom_buttom(
                text: "Apply",
                color: Color.fromARGB(255, 49, 148, 76),
                navigation: () {
                  FilterUniversities();
                }),
          ])
        ],
      ),
    );
  }

  Widget _buildTabItemEmpty() {
    return Container(
      padding: EdgeInsets.symmetric(vertical: 10, horizontal: 24),
      color: Colors.grey[300],
      child: Text(
        '',
        style: TextStyle(
          color: Color.fromARGB(255, 64, 62, 62),
          fontWeight: FontWeight.bold,
          fontSize: 30,
        ),
      ),
    );
  }

  sort_bottom_buttom(
      {required String text,
      required Color color,
      required Null Function() navigation}) {
    return Expanded(
      flex: 1,
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          padding: EdgeInsetsDirectional.symmetric(horizontal: 5, vertical: 20),
          side: BorderSide(
            width: 1.0,
            color: Color.fromARGB(255, 255, 255, 255),
          ),
          backgroundColor: Colors.white,
        ),
        onPressed: () {
          navigation();
        },
        child: Center(
          child: Text(
            text,
            style: TextStyle(
              color: color,
              fontSize: 20,
              fontFamily: "Roboto",
              fontWeight: FontWeight.w700,
            ),
          ),
        ),
      ),
    );
  }

  void FilterUniversities() {
    print(chooseoptions);

    List<String> ranking = [];
    List<String> cities = [];
    String rating = "";

    for (int i = 0; i < chooseoptions.length; i++) {
      if (uniqueranks.contains(chooseoptions[i])) {
        // Extract only the numeric part
        String numericPart = chooseoptions[i].replaceAll(RegExp(r'[^0-9]'), '');
        ranking.add(numericPart);
      } else if (uniquecities.contains(chooseoptions[i])) {
        cities.add(chooseoptions[i]);
      } else if (uniqueratings.contains(chooseoptions[i])) {
        // Extract only the numeric part
        String numericPart = chooseoptions[i].replaceAll(RegExp(r'[^0-9]'), '');
        rating = numericPart;
      }
    }

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => FilteredUniversities(
          ranking: ranking,
          cities: cities,
          rating: rating,
        ),
      ),
    );
  }
}

// SortOne Widget

class SortOne extends StatefulWidget {
  const SortOne({super.key});

  @override
  _SortOneState createState() => _SortOneState();
}

class _SortOneState extends State<SortOne> {
  Color checkcolor = Color(0xffE0DAD1);
  Color checkcolor1 = Color(0xffE0DAD1);
  Color checkcolor2 = Color(0xffE0DAD1);
  Color checkcolor3 = Color(0xffE0DAD1);
  Color checkcolor4 = Color(0xffE0DAD1);

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        SizedBox(
          height: MediaQuery.of(context).size.height * 0.8,
          child: ListView.builder(
            itemCount: uniqueratings.length,
            itemBuilder: (BuildContext context, int index) {
              return Container(
                decoration: BoxDecoration(
                  border: Border(
                    bottom: BorderSide(
                      color: Color.fromARGB(255, 224, 224, 224),
                      width: 1,
                    ),
                  ),
                ),
                padding: EdgeInsets.symmetric(vertical: 1, horizontal: 2),
                child: Row(
                  children: [
                    IconButton(
                        onPressed: () {
                          setState(() {
                            if (chooseoptions.contains(uniqueratings[index])) {
                              chooseoptions.remove(uniqueratings[index]);
                            } else {
                              chooseoptions.add(uniqueratings[index]);
                            }
                          });
                        },
                        icon: Icon(
                          Icons.check_circle,
                          color: chooseoptions.contains(uniqueratings[index])
                              ? Color.fromARGB(255, 17, 162, 63)
                              : Color.fromARGB(255, 224, 224, 224),
                        )),
                    Text(
                      uniqueratings[index],
                      style: TextStyle(
                        color: Colors.black,
                        fontWeight: FontWeight.w500,
                        fontSize: 20,
                        fontFamily: "Poppins",
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}

// SortTwo Widget

class SortTwo extends StatefulWidget {
  const SortTwo({super.key});

  @override
  _SortTwoState createState() => _SortTwoState();
}

class _SortTwoState extends State<SortTwo> {
  Color checkcolor11 = Color(0xffE0DAD1);
  Color checkcolor12 = Color(0xffE0DAD1);
  Color checkcolor13 = Color(0xffE0DAD1);
  Color checkcolor14 = Color(0xffE0DAD1);
  final TextEditingController _searchQueryController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        SizedBox(
          height: MediaQuery.of(context).size.height * 0.8,
          child: ListView.builder(
            itemCount: uniquecities.length,
            itemBuilder: (BuildContext context, int index) {
              return Container(
                decoration: BoxDecoration(
                  border: Border(
                    bottom: BorderSide(
                      color: Color.fromARGB(255, 224, 224, 224),
                      width: 1,
                    ),
                  ),
                ),
                padding: EdgeInsets.symmetric(vertical: 1, horizontal: 2),
                child: Row(
                  children: [
                    IconButton(
                        onPressed: () {
                          setState(() {
                            if (chooseoptions.contains(uniquecities[index])) {
                              chooseoptions.remove(uniquecities[index]);
                            } else {
                              chooseoptions.add(uniquecities[index]);
                            }
                          });
                        },
                        icon: Icon(
                          Icons.check_circle,
                          color: chooseoptions.contains(uniquecities[index])
                              ? Color.fromARGB(255, 17, 162, 63)
                              : Color.fromARGB(255, 224, 224, 224),
                        )),
                    Text(
                      uniquecities[index],
                      style: TextStyle(
                        color: Colors.black,
                        fontWeight: FontWeight.w500,
                        fontSize: 20,
                        fontFamily: "Poppins",
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}

// SortThree Widget

class SortThree extends StatefulWidget {
  const SortThree({super.key});

  @override
  _SortThreeState createState() => _SortThreeState();
}

class _SortThreeState extends State<SortThree> {
  Color checkcolor111 = Color(0xffE0DAD1);
  Color checkcolor112 = Color(0xffE0DAD1);
  Color checkcolor113 = Color(0xffE0DAD1);
  Color checkcolor114 = Color(0xffE0DAD1);

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        SizedBox(
          height: MediaQuery.of(context).size.height * 0.8,
          child: ListView.builder(
            itemCount: uniqueranks.length,
            itemBuilder: (BuildContext context, int index) {
              return Container(
                decoration: BoxDecoration(
                  border: Border(
                    bottom: BorderSide(
                      color: Color.fromARGB(255, 224, 224, 224),
                      width: 1,
                    ),
                  ),
                ),
                padding: EdgeInsets.symmetric(vertical: 1, horizontal: 2),
                child: Row(
                  children: [
                    IconButton(
                        onPressed: () {
                          setState(() {
                            if (chooseoptions.contains(uniqueranks[index])) {
                              chooseoptions.remove(uniqueranks[index]);
                            } else {
                              chooseoptions.add(uniqueranks[index]);
                            }
                          });
                        },
                        icon: Icon(
                          Icons.check_circle,
                          color: chooseoptions.contains(uniqueranks[index])
                              ? Color.fromARGB(255, 17, 162, 63)
                              : Color.fromARGB(255, 224, 224, 224),
                        )),
                    Text(
                      uniqueranks[index],
                      style: TextStyle(
                        color: Colors.black,
                        fontWeight: FontWeight.w500,
                        fontSize: 20,
                        fontFamily: "Poppins",
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}
