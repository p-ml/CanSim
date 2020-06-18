# CanSim
*Submission for EE40148 Group Design & Business Project, Detailed Design*

Back-end development for a prototype fleet monitoring device. Uses the [cannelloni](https://github.com/mguentner/cannelloni) framework to transmit and interpret CAN messages over ethernet, before forwarding them to the front-end GUI.

*canSim.py* provides a GUI to simulate CAN messages, to be run on device A.  
*canRec.py* interprets and reroutes the received CAN messages, to be run on device B.

*test_canSim.py* and *test_canRec.py* are the respective unit tests.

For the prototype demonstration, device A was an laptop running Ubuntu and device B was a Raspberry Pi 3B+. The devices were connected via ethernet.


Repository ownership transferred from university account (pm657) to personal account (p-ml) 15/6/20
 
