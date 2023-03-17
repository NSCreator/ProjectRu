// ignore_for_file: camel_case_types, non_constant_identifier_names

import 'dart:async';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:video_player/video_player.dart';



Future main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]).then((_) {
    runApp(const MaterialApp(home: HomePage(),debugShowCheckedModeBanner: false,));
  });
}
class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override


  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  bool isManualMode = false;
  final TextController = TextEditingController();
  DatabaseReference _databaseReference = FirebaseDatabase.instance.ref();
  @override
  void dispose() {
    TextController.dispose();
    super.dispose();
  }
  @override
  Widget build(BuildContext context) {
    return  Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                Color.fromRGBO(53, 166, 204, 1),
                Color.fromRGBO(24, 45, 74, 1),
                Color.fromRGBO(21, 47, 61, 1)
              ]),
        ),
        child: SafeArea(
          child:Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,

            children: [
              const Padding(
                padding: EdgeInsets.only(left: 10,top: 3,bottom: 3),
                child: Text("Project Ru ( Smart Robot )",style: TextStyle(fontSize: 25,fontWeight: FontWeight.w500),),
              ),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Container(
                  decoration: BoxDecoration(
                      color: Colors.blueGrey.shade100,
                      borderRadius: BorderRadius.circular(15),
                  ),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [

                          StreamBuilder<DocumentSnapshot>(
                            stream: FirebaseFirestore.instance.collection("sensors").doc("temp").snapshots(),
                            builder: (context, snapshot) {
                              if (snapshot.hasData) {
                                return Text("Temperature : ${snapshot.data!["value"]} °C ",style: const TextStyle(fontSize: 18),);
                              } else {
                                return const Text("Temperature : 0 °C",style: TextStyle(fontSize: 18),);
                              }
                            },
                          ),
                          StreamBuilder<DocumentSnapshot>(
                            stream: FirebaseFirestore.instance.collection("sensors").doc("ftemp").snapshots(),
                            builder: (context, snapshot) {
                              if (snapshot.hasData) {
                                return Text(": ${snapshot.data!["value"]} °F",style: const TextStyle(fontSize: 18),);
                              } else {
                                return const Text("error °F",style: TextStyle(fontSize: 18),);
                              }
                            },
                          ),
                          const SizedBox(width: 10,),
                          StreamBuilder<DocumentSnapshot>(
                            stream: FirebaseFirestore.instance.collection("sensors").doc("humi").snapshots(),
                            builder: (context, snapshot) {
                              if (snapshot.hasData) {
                                return Text("Humidity : ${snapshot.data!["value"]} %",style: const TextStyle(fontSize: 18),);
                              } else {
                                return const Text("Humidity : error %",style: const TextStyle(fontSize: 18),);
                              }
                            },
                          ),
                        ],
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [

                          StreamBuilder<DocumentSnapshot>(
                            stream: FirebaseFirestore.instance.collection("sensors").doc("temp").snapshots(),
                            builder: (context, snapshot) {
                              if (snapshot.hasData) {
                                return Text("Light : ${snapshot.data!["value"]} ",style: const TextStyle(fontSize: 18),);
                              } else {
                                return const Text("Light : error",style: TextStyle(fontSize: 18),);
                              }
                            },
                          ),
                          StreamBuilder<DocumentSnapshot>(
                            stream: FirebaseFirestore.instance.collection("sensors").doc("raspiTemp").snapshots(),
                            builder: (context, snapshot) {
                              if (snapshot.hasData) {
                                return Text("Raspi Temp : ${snapshot.data!["value"]} °C ",style: const TextStyle(fontSize: 18),);
                              } else {
                                return const Text("Temperature : 0 °C",style: TextStyle(fontSize: 18),);
                              }
                            },
                          ),

                        ],
                      ),
                      StreamBuilder<DocumentSnapshot>(
                        stream: FirebaseFirestore.instance.collection("sensors").doc("ic'sTemp").snapshots(),
                        builder: (context, snapshot) {
                          if (snapshot.hasData) {
                            return Text("IC'S Temp : ${snapshot.data!["value"]} ",style: const TextStyle(fontSize: 18),);
                          } else {
                            return const Text("Light : error",style: TextStyle(fontSize: 18),);
                          }
                        },
                      ),
                    ],
                  ),
                ),
              ),
              Expanded(
                child: SingleChildScrollView(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Padding(
                            padding: EdgeInsets.all(8.0),
                            child: Text("Live Video",style: const TextStyle(fontSize: 35,color: Colors.white)),
                          ),
                          const Spacer(),
                           InkWell(
                            child: Padding(
                              padding: EdgeInsets.only(right: 10,top: 20),
                              child: Text(TextController.text.trim()),
                            ),
                            onLongPress:(){
                              showDialog(
                                context: context,
                                builder: (context) {
                                  return Dialog(
                                    backgroundColor: Colors.black.withOpacity(0.3),
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                                    elevation: 16,
                                    child: Container(
                                      decoration: BoxDecoration(
                                        border: Border.all(color: Colors.tealAccent),
                                        borderRadius: BorderRadius.circular(20),
                                      ),
                                      child: ListView(
                                        shrinkWrap: true,
                                        children:  <Widget>[
                                          SizedBox(height: 10),
                                          Padding(
                                            padding: EdgeInsets.only(left: 15),
                                            child: Text(
                                              "Enter IP Address",
                                              style: TextStyle(color: Colors.white, fontWeight: FontWeight.w600, fontSize: 18),
                                            ),
                                          ),
                                          SizedBox(
                                            height: 5,
                                          ),
                                          Padding(
                                            padding: const EdgeInsets.only(left: 10, right: 10, top: 5, bottom: 5),
                                            child: Container(
                                              decoration: BoxDecoration(
                                                color: Colors.grey[200],
                                                border: Border.all(color: Colors.white),
                                                borderRadius: BorderRadius.circular(14),
                                              ),
                                              child: Padding(
                                                padding: const EdgeInsets.only(left: 20),
                                                child: TextFormField(
                                                  controller: TextController,
                                                  textInputAction: TextInputAction.next,
                                                  decoration: InputDecoration(
                                                    border: InputBorder.none,
                                                    hintText: 'Enter IP Address',
                                                  ),
                                                ),
                                              ),
                                            ),
                                          ),
                                          Center(
                                            child: InkWell(
                                              child: Container(
                                                decoration: BoxDecoration(
                                                  color: Colors.white,
                                                  borderRadius: BorderRadius.circular(20)
                                                ),
                                                child: Padding(
                                                  padding: const EdgeInsets.all(8.0),
                                                  child: Text("---OK---",style: TextStyle(color: Colors.black),),
                                                ),
                                              ),
                                              onTap: (){
                                                setState(() {

                                                });
                                              },
                                            ),
                                          ),
                                          SizedBox(
                                            height: 10,
                                          ),
                                        ],
                                      ),
                                    ),
                                  );
                                },
                              );
                            },
                          ),
                          Padding(
                            padding: const EdgeInsets.only(right: 10),
                            child: InkWell(
                              child: Container(
                                  decoration: BoxDecoration(
                                    borderRadius: BorderRadius.circular(20),
                                    color: Colors.black.withOpacity(0.3),
                                  ),
                                  child: Padding(
                                    padding: const EdgeInsets.all(8.0),
                                    child: const Text("OPEN",style: TextStyle(color: Colors.white,fontSize: 20),),
                                  )
                              ),
                              onTap:()async{
                                  final Uri urlIn = Uri.parse("http://${TextController.text}/");
                                  if (!await launchUrl(urlIn, mode: LaunchMode.externalApplication)) {
                                    throw 'Could not launch $urlIn';
                                  }
                              },
                            ),
                          ),
                        ],
                      ),
                      Row(
                        children: [
                          const Padding(
                            padding: EdgeInsets.all(8.0),
                            child: Text("Manual Controller",style: const TextStyle(fontSize: 35,color: Colors.white)),
                          ),
                          const Spacer(),
                          Padding(
                            padding: const EdgeInsets.only(right: 10),
                            child: InkWell(
                              child: Container(
                                decoration: BoxDecoration(
                                  borderRadius: BorderRadius.circular(5),
                                  color: isManualMode?Colors.green.withOpacity(0.3):Colors.red.withOpacity(0.3),
                                ),
                                child: Padding(
                                  padding: const EdgeInsets.all(8.0),
                                  child: isManualMode?const Text("--On--",style: const TextStyle(color: Colors.white,fontSize: 20),):const Text("--OFF--",style: TextStyle(color: Colors.white,fontSize: 20),),
                                )
                              ),
                              onTap:(){
                                setState(() {
                                  isManualMode = !isManualMode;
                                });
                              },
                            ),
                          ),
                        ],
                      ),
                      if(isManualMode)Row(
                        children: [
                          Flexible(
                            flex: 2,
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                const Padding(
                                  padding: EdgeInsets.all(8.0),
                                  child: Text("Wheels",style: TextStyle(fontSize: 25,color: Colors.white),),
                                ),
                                Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  Padding(
                                    padding: const EdgeInsets.all(5.0),
                                    child: Container(
                                      height: 55,
                                      width: 55,
                                      decoration: BoxDecoration(
                                        borderRadius: BorderRadius.circular(5),
                                        color: Colors.black.withOpacity(0.3),
                                      ),
                                      child: const Icon(Icons.keyboard_arrow_up,size: 55,color: Colors.white,),
                                    ),
                                  )
                                ],
                              ),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  crossAxisAlignment: CrossAxisAlignment.center,
                                  children: [
                                    Padding(
                                      padding: const EdgeInsets.all(5.0),
                                      child: Container(
                                        height: 55,
                                        width: 55,
                                        decoration: BoxDecoration(
                                          borderRadius: BorderRadius.circular(5),
                                          color: Colors.black.withOpacity(0.3),
                                        ),
                                        child: const Icon(Icons.keyboard_arrow_left,size: 55,color: Colors.white,),
                                      ),
                                    ),
                                    Padding(
                                      padding: const EdgeInsets.all(5.0),
                                      child: Container(
                                        height: 55,
                                        width: 55,
                                        decoration: BoxDecoration(
                                          borderRadius: BorderRadius.circular(5),
                                          color: Colors.black.withOpacity(0.3),
                                        ),
                                        child: const Icon(Icons.circle_outlined,size: 50,color: Colors.white,),
                                      ),
                                    ),
                                    Padding(
                                      padding: const EdgeInsets.all(5.0),
                                      child: Container(
                                        height: 55,
                                        width: 55,
                                        decoration: BoxDecoration(
                                          borderRadius: BorderRadius.circular(5),
                                          color: Colors.black.withOpacity(0.3),
                                        ),
                                        child: const Icon(Icons.keyboard_arrow_right,size: 55,color: Colors.white,),
                                      ),
                                    ),
                                  ],
                                ),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  crossAxisAlignment: CrossAxisAlignment.center,
                                  children: [
                                    Padding(
                                      padding: const EdgeInsets.all(5.0),
                                      child: Container(
                                        height: 55,
                                        width: 55,
                                        decoration: BoxDecoration(
                                          borderRadius: BorderRadius.circular(5),
                                          color: Colors.black.withOpacity(0.3),
                                        ),
                                        child: const Icon(Icons.keyboard_arrow_down,size: 55,color: Colors.white,),
                                      ),
                                    )
                                  ],
                                ),

                              ],
                            ),
                          ),
                          Flexible(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  const Padding(
                                    padding: EdgeInsets.all(8.0),
                                    child: Text("Camera",style: TextStyle(fontSize: 25,color: Colors.white),),
                                  ),
                                  Padding(
                                    padding: const EdgeInsets.all(5.0),
                                    child: Container(
                                      height: 30,
                                      width: 30,
                                      decoration: BoxDecoration(
                                        borderRadius: BorderRadius.circular(5),
                                        color: Colors.black.withOpacity(0.3),
                                      ),
                                      child: const Icon(Icons.keyboard_arrow_up,size: 30,color: Colors.white,),
                                    ),
                                  ),
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    crossAxisAlignment: CrossAxisAlignment.center,
                                    children: [
                                      Padding(
                                        padding: const EdgeInsets.all(5.0),
                                        child: Container(
                                          height: 30,
                                          width: 30,
                                          decoration: BoxDecoration(
                                            borderRadius: BorderRadius.circular(5),
                                            color: Colors.black.withOpacity(0.3),
                                          ),
                                          child: const Icon(Icons.keyboard_arrow_left,size: 30,color: Colors.white,),
                                        ),
                                      ),  Padding(
                                        padding: const EdgeInsets.all(5.0),
                                        child: Container(
                                          height: 30,
                                          width: 30,
                                          decoration: BoxDecoration(
                                            borderRadius: BorderRadius.circular(5),
                                            color: Colors.black.withOpacity(0.3),
                                          ),
                                          child: const Icon(Icons.circle_outlined,size: 30,color: Colors.white,),
                                        ),
                                      ),  Padding(
                                        padding: const EdgeInsets.all(5.0),
                                        child: Container(
                                          height: 30,
                                          width: 30,
                                          decoration: BoxDecoration(
                                            borderRadius: BorderRadius.circular(5),
                                            color: Colors.black.withOpacity(0.3),
                                          ),
                                          child: const Icon(Icons.keyboard_arrow_right,size: 30,color: Colors.white,),
                                        ),
                                      ),
                                    ],
                                  ),
                                  Padding(
                                    padding: const EdgeInsets.all(5.0),
                                    child: Container(
                                      height: 30,
                                      width: 30,
                                      decoration: BoxDecoration(
                                        borderRadius: BorderRadius.circular(5),
                                        color: Colors.black.withOpacity(0.3),
                                      ),
                                      child: const Icon(Icons.keyboard_arrow_down,size: 30,color: Colors.white,),
                                    ),
                                  ),
                                  Padding(
                                    padding: const EdgeInsets.all(5.0),
                                    child: Container(

                                      decoration: BoxDecoration(
                                        borderRadius: BorderRadius.circular(10),
                                        color: Colors.red.withOpacity(0.3),
                                      ),
                                      child: const Padding(
                                        padding: EdgeInsets.all(5.0),
                                        child: Text("change Camera",style: TextStyle(color: Colors.white),),
                                      ),
                                    ),
                                  ),
                                ],
                              )
                          )
                        ],
                      ),
                      StreamBuilder<List<smartLEDConvertor>>(
                        stream: readsmartLED(),
                        builder: (context, snapshot) {
                          final Books = snapshot.data;
                          switch (snapshot.connectionState) {
                            case ConnectionState.waiting:
                              return const Center(
                                  child: CircularProgressIndicator(
                                    strokeWidth: 0.3,
                                    color: Colors.cyan,
                                  ));
                            default:
                              if (snapshot.hasError) {
                                return const Center(child: Text('Error with TextBooks Data or\n Check Internet Connection'));
                              } else {
                                if (Books!.isEmpty) {

                                  return const Center(
                                    child: Padding(
                                      padding:  EdgeInsets.all(8.0),
                                      child: Text(
                                        "Other Projects are not available",
                                        style: TextStyle(color: Colors.blue),
                                      ),
                                    ),
                                  );
                                } else {
                                  return ListView.builder(
                                    physics: const BouncingScrollPhysics(),
                                    shrinkWrap: true,
                                    itemCount: Books.length,
                                    scrollDirection: Axis.vertical,
                                    itemBuilder: (BuildContext context, int index) {
                                      final SubjectsData = Books[index];
                                      return Padding(
                                        padding: const EdgeInsets.all(8.0),
                                        child: Container(
                                          width: double.infinity,
                                          decoration: BoxDecoration(
                                            borderRadius: BorderRadius.circular(20),
                                            color: SubjectsData.active?Colors.green.withOpacity(0.3):Colors.black.withOpacity(0.3),
                                          ),
                                          child: Column(
                                            mainAxisAlignment: MainAxisAlignment.start,
                                            crossAxisAlignment: CrossAxisAlignment.start,
                                            children: [
                                              Padding(
                                                padding: const EdgeInsets.all(8.0),
                                                child: Row(
                                                  children: [
                                                    Text(SubjectsData.name,style: const TextStyle(fontSize: 25,fontWeight: FontWeight.w500,color: Colors.white),),
                                                    const Spacer(),
                                                    Padding(
                                                      padding: const EdgeInsets.only(top: 20,right: 10),
                                                      child: Text("color : ${SubjectsData.color}",style: TextStyle(fontWeight: FontWeight.w500,color: Colors.white.withOpacity(0.8)),),
                                                    ),
                                                    InkWell(
                                                      child: Container(
                                                          decoration: BoxDecoration(
                                                            borderRadius: BorderRadius.circular(5),
                                                            color: SubjectsData.isOn?Colors.green.withOpacity(0.5):Colors.red.withOpacity(0.3),
                                                          ),
                                                          child: Padding(
                                                            padding: const EdgeInsets.all(8.0),
                                                            child: SubjectsData.isOn?const Text("--On--",style:  TextStyle(color: Colors.white,fontSize: 20),):const Text("--OFF--",style:  TextStyle(color: Colors.white,fontSize: 20),),
                                                          )
                                                      ),
                                                      onTap:(){
                                                        if(SubjectsData.isOn){
                                                          FirebaseFirestore.instance.collection("SmartLED").doc(SubjectsData.id).update({
                                                            "isOn":false
                                                          });
                                                          _databaseReference.child("isOn").set(false);
                                                        }else{
                                                          FirebaseFirestore.instance.collection("SmartLED").doc(SubjectsData.id).update({
                                                            "isOn":true
                                                          });
                                                          _databaseReference.child("isOn").set(true);

                                                        }
                                                      },
                                                    ),
                                                  ],
                                                ),
                                              ),
                                              Padding(
                                                padding: const EdgeInsets.only(left: 8,right: 8,bottom: 5),
                                                child: Row(
                                                  children: [
                                                    const Text("Timer : ",style: const TextStyle(fontSize: 25,fontWeight: FontWeight.w500,color: Colors.white),),
                                                    const Spacer(),
                                                    Text("${SubjectsData.timer} Mins",style: const TextStyle(fontSize: 25,fontWeight: FontWeight.w500,color: Colors.white),),
                                                    const Spacer(),
                                                    InkWell(
                                                      child: Container(
                                                          decoration: BoxDecoration(
                                                            borderRadius: BorderRadius.circular(20),
                                                            color: isManualMode?Colors.green.withOpacity(0.3):Colors.red.withOpacity(0.3),
                                                          ),
                                                          child: const Padding(
                                                            padding: EdgeInsets.all(8.0),
                                                            child:Text("Change",style: TextStyle(fontSize: 15,color: Colors.white),),
                                                          )
                                                      ),
                                                      onTap:(){


                                                        FirebaseFirestore.instance.collection("SmartLED").doc(SubjectsData.id).update({
                                                          "timer":"10"
                                                        });
                                                      },
                                                    ),
                                                  ],
                                                ),
                                              ),
                                              Padding(
                                                padding: const EdgeInsets.only(left: 20,right: 20,bottom: 5),
                                                child: Row(
                                                  children: [
                                                    Padding(
                                                      padding: const EdgeInsets.only(left: 3,right: 3),
                                                      child: InkWell(
                                                        child: Container(
                                                            decoration: BoxDecoration(
                                                              borderRadius: BorderRadius.circular(20),
                                                              color:Colors.white.withOpacity(0.5),
                                                            ),
                                                            child: const Padding(
                                                              padding: EdgeInsets.all(8.0),
                                                              child:Text("White",style: const TextStyle(fontSize: 15,color: Colors.black,fontWeight: FontWeight.bold),),
                                                            )
                                                        ),
                                                        onTap:(){
                                                          FirebaseFirestore.instance.collection("SmartLED").doc(SubjectsData.id).update({
                                                            "RGB":"(255,255,255)",
                                                            "color":"White"
                                                          });
                                                        },
                                                      ),
                                                    ),
                                                    const Spacer(),
                                                    Padding(
                                                      padding: const EdgeInsets.only(left: 3,right: 3),
                                                      child: InkWell(
                                                        child: Container(
                                                            decoration: BoxDecoration(
                                                              borderRadius: BorderRadius.circular(20),
                                                              color:Colors.red.withOpacity(0.5),
                                                            ),
                                                            child: const Padding(
                                                              padding: EdgeInsets.all(8.0),
                                                              child:Text("Red",style: const TextStyle(fontSize: 15,color: Colors.white,fontWeight: FontWeight.bold),),
                                                            )
                                                        ),
                                                        onTap:(){
                                                          FirebaseFirestore.instance.collection("SmartLED").doc(SubjectsData.id).update({
                                                            "RGB":"(255,0,0)",
                                                            "color":"Red"
                                                          });
                                                        },
                                                      ),
                                                    ),
                                                    const Spacer(),
                                                    Padding(
                                                      padding: const EdgeInsets.only(left: 3,right: 3),
                                                      child: InkWell(
                                                        child: Container(
                                                            decoration: BoxDecoration(
                                                              borderRadius: BorderRadius.circular(20),
                                                              color:Colors.green.withOpacity(0.5),
                                                            ),
                                                            child: const Padding(
                                                              padding: EdgeInsets.all(8.0),
                                                              child:Text("Green",style: const TextStyle(fontSize: 15,color: Colors.white,fontWeight: FontWeight.bold),),
                                                            )
                                                        ),
                                                        onTap:(){
                                                          FirebaseFirestore.instance.collection("SmartLED").doc(SubjectsData.id).update({
                                                            "RGB":"(0,255,0)",
                                                            "color":"Green"
                                                          });
                                                        },
                                                      ),
                                                    ),
                                                    const Spacer(),
                                                    Padding(
                                                      padding: const EdgeInsets.only(left: 3,right: 3),
                                                      child: InkWell(
                                                        child: Container(
                                                            decoration: BoxDecoration(
                                                              borderRadius: BorderRadius.circular(20),
                                                              color:Colors.blue.withOpacity(0.5),
                                                            ),
                                                            child: const Padding(
                                                              padding: EdgeInsets.all(8.0),
                                                              child:Text("Blue",style: const TextStyle(fontSize: 15,color: Colors.white,fontWeight: FontWeight.bold),),
                                                            )
                                                        ),
                                                        onTap:(){
                                                          FirebaseFirestore.instance.collection("SmartLED").doc(SubjectsData.id).update({
                                                            "RGB":"(0,0,255)",
                                                            "color":"Blue"
                                                          });
                                                        },
                                                      ),
                                                    ),
                                                    const Spacer(),
                                                    Padding(
                                                      padding: const EdgeInsets.only(left: 3,right: 3),
                                                      child: InkWell(
                                                        child: Container(
                                                            decoration: BoxDecoration(
                                                              borderRadius: BorderRadius.circular(20),
                                                              color:Colors.yellow.withOpacity(0.5),
                                                            ),
                                                            child: const Padding(
                                                              padding: EdgeInsets.all(8.0),
                                                              child:Text("Yellow",style: TextStyle(fontSize: 15,color: Colors.white,fontWeight: FontWeight.bold),),
                                                            )
                                                        ),
                                                        onTap:(){
                                                          FirebaseFirestore.instance.collection("SmartLED").doc(SubjectsData.id).update({
                                                            "RGB":"255,255,0",
                                                            "color":"Blue"
                                                          });
                                                        },
                                                      ),
                                                    ),
                                                  ],
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                      );

                                    },

                                  );

                                }
                              }
                          }
                        },
                      ),

                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Row(
                          children:  [
                            const Text("Add Remainder",style: TextStyle(fontSize: 25,color: Colors.white)),
                            const Spacer(),
                            Container(
                              decoration: BoxDecoration(
                              color: Colors.blueGrey.shade100,
                              borderRadius: BorderRadius.circular(15),
                            ),
                            child: Row(
                              children: const [
                                Padding(
                                  padding: EdgeInsets.all(3.0),
                                  child: Text("ADD",style: TextStyle(color: Colors.red,fontSize: 18),),
                                ),
                                Icon(Icons.add,size: 23,color: Colors.red,)
                              ],
                            ),)
                          ],
                        ),
                      ),
                      StreamBuilder<List<photosConvertor>>(
                        stream: readphotos(),
                        builder: (context, snapshot) {
                          final Books = snapshot.data;
                          switch (snapshot.connectionState) {
                            case ConnectionState.waiting:
                              return const Center(
                                  child: CircularProgressIndicator(
                                    strokeWidth: 0.3,
                                    color: Colors.cyan,
                                  ));
                            default:
                              if (snapshot.hasError) {
                                return const Center(child: Text('Error with TextBooks Data or\n Check Internet Connection'));
                              } else {
                                if (Books!.isEmpty) {

                                  return const Center(
                                    child: Padding(
                                      padding:  EdgeInsets.all(8.0),
                                      child: Text(
                                        "Other Projects are not available",
                                        style: TextStyle(color: Colors.blue),
                                      ),
                                    ),
                                  );
                                } else {
                                  return Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      const Padding(
                                        padding: EdgeInsets.only(left: 10, top: 20),
                                        child: Text(
                                          "Photos :",
                                          style: TextStyle(fontSize: 30, fontWeight: FontWeight.w500,color: Colors.black,),
                                        ),
                                      ),
                                      Container(
                                        height: 148,
                                        child: ListView.builder(
                                          physics: const BouncingScrollPhysics(),
                                          shrinkWrap: true,
                                          itemCount: Books.length,
                                          scrollDirection: Axis.vertical,
                                          itemBuilder: (BuildContext context, int index) {
                                            final SubjectsData = Books[index];
                                           return Column(
                                             mainAxisAlignment: MainAxisAlignment.start,
                                             crossAxisAlignment: CrossAxisAlignment.start,
                                             children: [
                                               Padding(
                                                 padding: const EdgeInsets.only(left: 10,bottom: 5,top: 3),
                                                 child: Text(SubjectsData.name,style: const TextStyle(fontSize: 18),),
                                               ),
                                               StreamBuilder<List<photoConvertor>>(
                                                 stream: readphoto(SubjectsData.id),
                                                 builder: (context, snapshot) {
                                                   final Books = snapshot.data;
                                                   switch (snapshot.connectionState) {
                                                     case ConnectionState.waiting:
                                                       return const Center(
                                                           child: CircularProgressIndicator(
                                                             strokeWidth: 0.3,
                                                             color: Colors.cyan,
                                                           ));
                                                     default:
                                                       if (snapshot.hasError) {
                                                         return const Center(child: Text('Error with TextBooks Data or\n Check Internet Connection'));
                                                       } else {
                                                         if (Books!.isEmpty) {

                                                           return const Center(
                                                             child: Padding(
                                                               padding:  EdgeInsets.all(8.0),
                                                               child: Text(
                                                                 "Other Projects are not available",
                                                                 style: TextStyle(color: Colors.blue),
                                                               ),
                                                             ),
                                                           );
                                                         } else {
                                                           return SizedBox(
                                                             height: 108,
                                                             child: ListView.builder(
                                                               physics: const BouncingScrollPhysics(),
                                                               shrinkWrap: true,
                                                               itemCount: Books.length,
                                                               scrollDirection: Axis.horizontal,
                                                               itemBuilder: (BuildContext context, int index) {
                                                                 final SubjectsData = Books[index];
                                                                 return Padding(
                                                                   padding: const EdgeInsets.only(left: 8),
                                                                   child: Container(
                                                                     height: 108,
                                                                     width: 170,
                                                                     alignment: Alignment.center,
                                                                     decoration: BoxDecoration(
                                                                         color: Colors.black54,
                                                                         borderRadius: BorderRadius.circular(15),
                                                                         image:  DecorationImage(
                                                                           image: NetworkImage(
                                                                             SubjectsData.url,
                                                                           ),
                                                                           fit: BoxFit.cover,
                                                                         )
                                                                     ),
                                                                     child: Column(
                                                                       children: [
                                                                         Row(
                                                                           children: [
                                                                             Align(
                                                                               alignment: Alignment.topLeft,
                                                                               child: Padding(
                                                                                 padding: const EdgeInsets.all(3.0),
                                                                                 child: Container(
                                                                                   decoration: BoxDecoration(
                                                                                     color: Colors.black.withOpacity(0.1),
                                                                                     borderRadius: BorderRadius.circular(15),

                                                                                   ),
                                                                                 ),
                                                                               ),

                                                                             ),
                                                                             const Spacer(),

                                                                           ],
                                                                         ),

                                                                         const Spacer(),
                                                                         Align(
                                                                           alignment: Alignment.bottomLeft,
                                                                           child: Container(
                                                                             decoration: BoxDecoration(
                                                                               color: Colors.black.withOpacity(0.4),
                                                                               borderRadius: BorderRadius.circular(15),

                                                                             ),
                                                                             child: Padding(
                                                                               padding:  const EdgeInsets.all(4.0),
                                                                               child: Text(SubjectsData.name,style: const TextStyle(fontWeight: FontWeight.w400,fontSize: 16,color: Colors.white), maxLines: 2,
                                                                                 overflow: TextOverflow.ellipsis,),
                                                                             ),
                                                                           ),

                                                                         ),
                                                                       ],
                                                                     ),
                                                                   ),
                                                                 );

                                                               },

                                                             ),
                                                           );
                                                         }
                                                       }
                                                   }
                                                 },
                                               ),
                                             ],
                                           );

                                          },

                                        ),
                                      ),

                                    ],
                                  );
                                }
                              }
                          }
                        },
                      ),
                      StreamBuilder<List<photoConvertor>>(
                        stream: readvideos(),
                        builder: (context, snapshot) {
                          final Books = snapshot.data;
                          switch (snapshot.connectionState) {
                            case ConnectionState.waiting:
                              return const Center(
                                  child: CircularProgressIndicator(
                                    strokeWidth: 0.3,
                                    color: Colors.cyan,
                                  ));
                            default:
                              if (snapshot.hasError) {
                                return const Center(child: Text('Error with TextBooks Data or\n Check Internet Connection'));
                              } else {
                                if (Books!.isEmpty) {

                                  return const Center(
                                    child: Padding(
                                      padding:  EdgeInsets.all(8.0),
                                      child: Text(
                                        "Other Projects are not available",
                                        style: TextStyle(color: Colors.blue),
                                      ),
                                    ),
                                  );
                                } else {
                                  return Column(
                                    mainAxisAlignment: MainAxisAlignment.start,
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      const Padding(
                                        padding: EdgeInsets.only(left: 10),
                                        child: Text(
                                          "Videos :",
                                          style: TextStyle(fontSize: 30, fontWeight: FontWeight.w500,color: Colors.black,),
                                        ),
                                      ),
                                      SizedBox(
                                        height: 108,
                                        child: ListView.builder(
                                          physics: const BouncingScrollPhysics(),
                                          shrinkWrap: true,
                                          itemCount: Books.length,
                                          scrollDirection: Axis.horizontal,
                                          itemBuilder: (BuildContext context, int index) {
                                            final SubjectsData = Books[index];
                                            return Padding(
                                              padding: const EdgeInsets.only(left: 8),
                                              child: InkWell(
                                                child: Container(
                                                  height: 108,
                                                  width: 170,
                                                  alignment: Alignment.center,
                                                  decoration: BoxDecoration(
                                                      color: Colors.black54,
                                                      borderRadius: BorderRadius.circular(15),
                                                      image: const DecorationImage(
                                                        image: NetworkImage(
                                                          "https://www.oasisalignment.com/wp-content/uploads/2018/07/video-icon.png",
                                                        ),
                                                        fit: BoxFit.cover,
                                                      )
                                                  ),
                                                  child: Column(
                                                    mainAxisAlignment: MainAxisAlignment.start,
                                                    crossAxisAlignment: CrossAxisAlignment.start,
                                                    children: [

                                                      Row(
                                                        mainAxisAlignment: MainAxisAlignment.start,
                                                        crossAxisAlignment: CrossAxisAlignment.start,
                                                        children: [
                                                          Align(
                                                            alignment: Alignment.topLeft,
                                                            child: Padding(
                                                              padding: const EdgeInsets.all(3.0),
                                                              child: Container(
                                                                decoration: BoxDecoration(
                                                                  color: Colors.black.withOpacity(0.1),
                                                                  borderRadius: BorderRadius.circular(15),

                                                                ),
                                                              ),
                                                            ),

                                                          ),
                                                          const Spacer(),

                                                        ],
                                                      ),

                                                      const Spacer(),
                                                      Align(
                                                        alignment: Alignment.bottomLeft,
                                                        child: Container(
                                                          decoration: BoxDecoration(
                                                            color: Colors.black.withOpacity(0.4),
                                                            borderRadius: BorderRadius.circular(15),

                                                          ),
                                                          child: Padding(
                                                            padding:  const EdgeInsets.all(4.0),
                                                            child: Text(SubjectsData.name,style: const TextStyle(fontWeight: FontWeight.w400,fontSize: 16,color: Colors.white), maxLines: 2,
                                                              overflow: TextOverflow.ellipsis,),
                                                          ),
                                                        ),

                                                      ),
                                                    ],
                                                  ),
                                                ),
                                                onTap: ()async{
                                                  final Uri urlIn = Uri.parse(SubjectsData.url);
                                                  if (!await launchUrl(urlIn, mode: LaunchMode.externalApplication))
                                                  throw 'Could not launch $urlIn';
                                                },
                                              ),
                                            );

                                          },

                                        ),
                                      ),
                                    ],
                                  );
                                }
                              }
                          }
                        },
                      ),
                    ],
                  ),
                ),
              ),
            ],
          )
        ),
      ),
    );
  }
}

class photoConvertor {
  String id;
  final String name, url;
  photoConvertor(
      {
        this.id = "",
        required this.name,
        required this.url
       });

  Map<String, dynamic> toJson() => {
    "id": id,
    "name": name,
    "url": url,
  };

  static photoConvertor fromJson(Map<String, dynamic> json) =>
      photoConvertor(

          id: json['id'],
          name: json["name"],
          url: json["url"]
      );
}

Stream<List<smartLEDConvertor>> readsmartLED() =>
    FirebaseFirestore.instance
        .collection('SmartLED')
        .orderBy("id", descending: false)
        .snapshots()
        .map((snapshot) => snapshot.docs
        .map((doc) => smartLEDConvertor.fromJson(doc.data()))
        .toList());

class smartLEDConvertor {
  String id;
  final String name,RGB,timer,color;
  bool isOn,active;
  smartLEDConvertor(
      {
        this.id = "",
        required this.name,
        required this.color,
        required this.isOn,
        required this.RGB,
        required this.timer,
        required this.active
      });

  Map<String, dynamic> toJson() => {
    "id": id,
    "name": name,
    "RGB":RGB,
    "timer":timer,
    "color":color,
    "isOn":isOn,
    "active":active
  };

  static smartLEDConvertor fromJson(Map<String, dynamic> json) =>
      smartLEDConvertor(
        id: json['id'],
        name: json["name"],
        color:json['color'],
        timer: json['timer'],
        RGB: json['RGB'],
        isOn: json['isOn'],
        active: json['active']
      );
}


Stream<List<photoConvertor>> readphoto(String id) =>
    FirebaseFirestore.instance
        .collection('360Photos').doc(id).collection("photos")
        .orderBy("id", descending: false)
        .snapshots()
        .map((snapshot) => snapshot.docs
        .map((doc) => photoConvertor.fromJson(doc.data()))
        .toList());

class photosConvertor {
  String id;
  final String name;
  photosConvertor(
      {
        this.id = "",
        required this.name,
      });

  Map<String, dynamic> toJson() => {
    "id": id,
    "name": name,
  };

  static photosConvertor fromJson(Map<String, dynamic> json) =>
      photosConvertor(
          id: json['id'],
          name: json["name"],
      );
}

Stream<List<photosConvertor>> readphotos() =>
    FirebaseFirestore.instance
        .collection('360Photos')
        .orderBy("id", descending: false)
        .snapshots()
        .map((snapshot) => snapshot.docs
        .map((doc) => photosConvertor.fromJson(doc.data()))
        .toList());
Stream<List<photoConvertor>> readvideos() =>
    FirebaseFirestore.instance
        .collection('360Videos')
        .orderBy("id", descending: false)
        .snapshots()
        .map((snapshot) => snapshot.docs
        .map((doc) => photoConvertor.fromJson(doc.data()))
        .toList());

