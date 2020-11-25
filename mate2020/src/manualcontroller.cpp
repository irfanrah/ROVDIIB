#include <iostream>
#include <ros/ros.h>
#include <sensor_msgs/Joy.h>
#include <mavros_msgs/OverrideRCIn.h>

using namespace std;

ros::Publisher override_publisher;

int currentspeedmaju = 1600;
int currentspeedmundur = 1400;
int kiridepan = 1;
int kanandepan = 2;
int kiribelakang = 0;
int kananbelakang = 3;
int kiriatas = 4;
int kananatas = 7;

void joyCallback(const sensor_msgs::Joy::ConstPtr& msg) {
    if (msg->axes[1] == 1) { //analog kiri(atas)
        mavros_msgs::OverrideRCIn rcin;
        for(int i=0; i<=7; i++){rcin.channels[i] = 1500;}
        rcin.channels[kiridepan] = currentspeedmaju;
        rcin.channels[kanandepan] = currentspeedmaju;
        rcin.channels[kiribelakang] = currentspeedmaju;
        rcin.channels[3] = currentspeedmaju;
        override_publisher.publish(rcin);
        ROS_INFO("Maju");
    }  else if (msg->axes[0] == -1) { //analog kiri(kanan)
        mavros_msgs::OverrideRCIn rcin;
        for(int i=0; i<=7; i++){rcin.channels[i] = 1500;}
        rcin.channels[kiridepan] = currentspeedmaju;
        rcin.channels[kanandepan] = currentspeedmundur;
        rcin.channels[kiribelakang] = currentspeedmundur ;
        rcin.channels[kananbelakang] = currentspeedmaju;
        override_publisher.publish(rcin);
        ROS_INFO("Geser Kanan");
    } else if (msg->axes[0] == 1) { //analog kiri(kiri)
        mavros_msgs::OverrideRCIn rcin;
        for(int i=0; i<=7; i++){rcin.channels[i] = 1500;}
        rcin.channels[kiridepan] = currentspeedmundur ;
        rcin.channels[kanandepan] = currentspeedmaju;
        rcin.channels[kiribelakang] = currentspeedmaju;
        rcin.channels[kananbelakang] = currentspeedmundur ;
        override_publisher.publish(rcin);
        ROS_INFO("Geser Kiri");
    } else if (msg->axes[1] == -1) { //analog kiri(atas)
        mavros_msgs::OverrideRCIn rcin;
        for(int i=0; i<=7; i++){rcin.channels[i] = 1500;}
        rcin.channels[kiridepan] = currentspeedmundur;
        rcin.channels[kanandepan] = currentspeedmundur;
        rcin.channels[kiribelakang] = currentspeedmundur;
        rcin.channels[kananbelakang] = currentspeedmundur;
        override_publisher.publish(rcin);
        ROS_INFO("Mundur");
    } else if (msg->axes[4] == 1) { //analog kanan(atas)
        mavros_msgs::OverrideRCIn rcin;
        for(int i=0; i<=7; i++){rcin.channels[i] = 1500;}
        rcin.channels[kiriatas] = currentspeedmaju;
        rcin.channels[kananatas] = currentspeedmaju;
        override_publisher.publish(rcin);
        ROS_INFO("Naik");
    } else if (msg->axes[4] == -1) { //analog kanan(bawah)
        mavros_msgs::OverrideRCIn rcin;
        for(int i=0; i<=7; i++){rcin.channels[i] = 1500;}
        rcin.channels[kiriatas] = currentspeedmundur;
        rcin.channels[kananatas] = currentspeedmundur;
        override_publisher.publish(rcin);
        ROS_INFO("Turun");
    } else if (msg->axes[3] == -1) { //analog kanan(kanan)
        mavros_msgs::OverrideRCIn rcin;
        for(int i=0; i<=7; i++){rcin.channels[i] = 1500;}
        rcin.channels[kiridepan] = currentspeedmaju;
        rcin.channels[kanandepan] = currentspeedmundur;
        rcin.channels[kiribelakang] = currentspeedmaju;
        rcin.channels[kananbelakang] = currentspeedmundur;
        override_publisher.publish(rcin);
        ROS_INFO("Putar Kanan");
    } else if (msg->axes[3] == 1) { //analog kanan(kiri)
        mavros_msgs::OverrideRCIn rcin;
        for(int i=0; i<=7; i++){rcin.channels[i] = 1500;}
        rcin.channels[kiridepan] = currentspeedmundur;
        rcin.channels[kanandepan] = currentspeedmaju;
        rcin.channels[kiribelakang] = currentspeedmundur;
        rcin.channels[kananbelakang] = currentspeedmaju;
        override_publisher.publish(rcin);
        ROS_INFO("Putar Kiri");
    } else if (msg->buttons[0]== 1) { //X Tambah kecepatan
        currentspeedmaju += 50;
        if (currentspeedmaju > 1900){currentspeedmaju = 1900;}
        currentspeedmundur -= 50;
        if (currentspeedmundur < 1100){currentspeedmundur = 1100;}  
        cout << "CurrentSpeed maju = " << currentspeedmaju << endl;
        cout << "CurrentSpeed mundur = " << currentspeedmundur << endl;
    } else if (msg->buttons[2]== 1) { //Segitiga Kurangi kecepatan maju
        currentspeedmaju -= 50;
        if (currentspeedmaju < 1550){currentspeedmaju = 1550;} 
        currentspeedmundur += 50;
        if (currentspeedmundur > 1450){currentspeedmundur = 1450;}
        cout << "CurrentSpeed maju = " << currentspeedmaju << endl; 
        cout << "CurrentSpeed mundur = " << currentspeedmundur << endl;
    } else{
        mavros_msgs::OverrideRCIn rcin;
        for(int i=0; i<=7; i++){rcin.channels[i] = 1500;}
        override_publisher.publish(rcin);
        ROS_INFO("Diem");
    }
}


int main(int argc, char **argv) {
    ros::init(argc, argv, "testservo");
    ros::NodeHandle nh;

    override_publisher = nh.advertise<mavros_msgs::OverrideRCIn>("/mavros/rc/override", 8);

    ros::Subscriber joy_subscriber = nh.subscribe("joy", 8, joyCallback);
    ros::spin();

}
