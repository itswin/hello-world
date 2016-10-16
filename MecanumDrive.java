package org.firstinspires.ftc.teamcode;

import com.qualcomm.robotcore.eventloop.opmode.OpMode;
import com.qualcomm.robotcore.eventloop.opmode.TeleOp;
import com.qualcomm.robotcore.hardware.DcMotor;
import com.qualcomm.robotcore.util.Range;

/**
 * Created by Winston on 10/16/2016.
 */
@TeleOp(name="Mecanum Driver", group="TeleOp")
public class MecanumDrive extends OpMode
{
    private DcMotor frontRightMotor;
    private DcMotor backRightMotor;
    private DcMotor frontLeftMotor;
    private DcMotor backLeftMotor;
    private DcMotor rollerMotor;

    public void init()
    {
        frontRightMotor = hardwareMap.dcMotor.get("frontRightMotor");
        backRightMotor = hardwareMap.dcMotor.get("backRightMotor");
        frontLeftMotor = hardwareMap.dcMotor.get("frontLeftMotor");
        backLeftMotor = hardwareMap.dcMotor.get("backLeftMotor");
        rollerMotor = hardwareMap.dcMotor.get("rollerMotor");

        backRightMotor.setDirection(DcMotor.Direction.REVERSE);
        backLeftMotor.setDirection(DcMotor.Direction.REVERSE);
    }

    public void loop()
    {
        /*
         * Gamepad 1
        */

        /* Mecanum Drive
         * note that if y equal -1 then joystick is pushed all of the way forward.
         * Left Y moves forward/backward
         * Left X moves left/right
         * Right X rotates
         */
        float drive = threshold(-gamepad1.left_stick_y, .05);
        float strafe = threshold(gamepad1.left_stick_x, .05);
        float rotate = threshold(gamepad1.right_stick_x, .05);

        float frontLeft = drive + strafe + rotate;
        float backLeft = drive - strafe + rotate;
        float frontRight = drive - strafe - rotate;
        float backRight = drive + strafe - rotate;

        frontLeft = (float)(scaleInput(frontLeft));
        backLeft = (float)(scaleInput(backLeft));
        frontRight = (float)(scaleInput(frontRight));
        backRight = (float)(scaleInput(backRight));

        frontLeft = Range.clip(frontLeft, -1, 1);
        backLeft = Range.clip(backLeft, -1, 1);
        frontRight = Range.clip(frontRight, -1, 1);
        backRight = Range.clip(backRight, -1, 1);

        //Write power to motors
        frontRightMotor.setPower(frontRight);
        backRightMotor.setPower(backRight);

        frontLeftMotor.setPower(frontLeft);
        backLeftMotor.setPower(backLeft);

        float roller = gamepad1.right_bumper ? 1 : 0;
        roller = gamepad1.left_bumper ? -1 : roller;

        rollerMotor.setPower(roller);

        //Telemetry
        telemetry.addData("Right Motors", String.format("%.2f | %.2f", frontRight, backRight));
        telemetry.addData("Left Motors", String.format("%.2f | %.2f", frontLeft, backLeft));
    }

    /*
     * Code to run when the op mode is first disabled goes here
     *
     * @see com.qualcomm.robotcore.eventloop.opmode.OpMode#stop()
     */
    @Override
    public void stop() {

    }


    /*
     * This method scales the joystick input so for low joystick values, the
     * scaled value is less than linear.  This is to make it easier to drive
     * the robot more precisely at slower speeds.
     */
    private double scaleInput(double dVal)  {
        double[] scaleArray = { 0.0, 0.05, 0.09, 0.10, 0.12, 0.15, 0.18, 0.24,
                0.30, 0.36, 0.43, 0.50, 0.60, 0.72, 0.85, 1.00, 1.00 };

        // get the corresponding index for the scaleInput array.
        int index = (int) (dVal * 16.0);

        // index should be positive.
        if (index < 0) {
            index = -index;
        }

        // index cannot exceed size of array minus 1.
        if (index > 16) {
            index = 16;
        }

        // get value from the array.
        double dScale;
        if (dVal < 0) {
            dScale = -scaleArray[index];
        } else {
            dScale = scaleArray[index];
        }

        // return scaled value.
        return dScale;
    }

    /**
     * Turn the bot by the given degrees
     * Positive is CW, negative is CCW
     * Best guess at loop length and motor power
     * @param degreesToTurn number of degrees to turn
     */
    private void turn(double degreesToTurn)
    {
        // TODO Tweak loop length and motor power for turning (find best fit line???)
        for(int i = 0; i < 580 * Math.abs(degreesToTurn); i++) {
            frontRightMotor.setPower(degreesToTurn > 0 ? 1 : -1);
            backRightMotor.setPower(degreesToTurn > 0 ? 1 : -1);
            frontLeftMotor.setPower(degreesToTurn > 0 ? -1 : 1);
            backLeftMotor.setPower(degreesToTurn > 0 ? -1 : 1);
        }
    }

    private float threshold(float val, double threshold)
    {
        return Math.abs(val) > threshold ? val : 0;
    }
}