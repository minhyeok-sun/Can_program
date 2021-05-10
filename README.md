# Can_program
* 연구실 차량 kia Niro 차량, kia K7 simulator, mobileye의 Can_data 수집 프로그램
* ubuntu 18.04, ros-melodic 기반 작성
* Kvaser can leaf 장비 활용

1) k7, niro, mobileye_listner.py : 각 차량에서 받은 Can_Raw data publish하는 노드 코드
2) k7, niro, mobileye_converter.py : 각 Can_Raw data를 통해 rpm, speed, steering-angel 등 data로 decode하는 노드
3) niro_uds.py : 실차량 kia niro의 uds_data(D_CAN), OBD2 수집 코드
4) mobileye_detection.py : mobileye에서 감지한 주변 차량에 대한 data 수집 코드
5) mobileye_detection_visual.py : 4)코드에서 opencv를 통해 시각화한 image 출력 코드
6) steering_niro2k7.py : 실차량 niro에서 logging한 steering-angle 정보를 연구실 내 K7 simulator handle 에 출력하는 코드
