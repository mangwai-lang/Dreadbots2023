// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot;

import com.kauailabs.navx.frc.AHRS;

import edu.wpi.first.wpilibj2.command.Command;
import frc.robot.Constants.OperatorConstants;
import frc.robot.commands.Autos;
import frc.robot.commands.DriveCommand;
import frc.robot.commands.BalanceCommand;
import frc.robot.commands.TurboCommand;
import frc.robot.commands.TurtleCommand;
import frc.robot.subsystems.Drive;
import util.controls.DreadbotController;
import edu.wpi.first.wpilibj.SerialPort;

/**
 * This class is where the bulk of the robot should be declared. Since Command-based is a
 * "declarative" paradigm, very little robot logic should actually be handled in the {@link Robot}
 * periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
 * subsystems, commands, and trigger mappings) should be declared here.
 */
public class RobotContainer {

  private final AHRS gyro = new AHRS(SerialPort.Port.kMXP);
 private final Drive drive = new Drive();
  private final DreadbotController primaryController = new DreadbotController(OperatorConstants.PRIMARY_JOYSTICK_PORT);

    /**
     * The container for the robot. Contains subsystems, OI devices, and commands.
     */
    public RobotContainer() {
        // Configure the trigger bindings
        configureBindings();
    }

  private void configureBindings() {
    DriveCommand driveCommand = new DriveCommand(drive, primaryController::getYAxis, primaryController::getXAxis);
    drive.setDefaultCommand(driveCommand); 
    primaryController.getXButton().whileTrue(new BalanceCommand(drive, gyro));
    primaryController.getLeftBumper().whileTrue(new TurtleCommand(driveCommand));
    primaryController.getRightBumper().whileTrue(new TurboCommand(driveCommand));
   // if button x is pressed

    // drive.setCommand(RobotBalancCommand)
  }
  /**
   * Use this to pass the autonomous command to the main {@link Robot} class.
   *
   * @return the command to run in autonomous
   */
  public Command getAutonomousCommand() {
    // An example command will be run in autonomous
    return Autos.Auton(drive);
  }
}
