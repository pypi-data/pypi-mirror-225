from qcodes import VisaInstrument

class ZM2376(VisaInstrument):
    """
    This class represents the ZM2376 instrument and inherits from the `VisaInstrument` class in qcodes.
    It provides functionality for controlling and performing measurements with the ZM2376 instrument.
    """

    ERROR_STATEMENTS = {
        0: None,  # No error
        1: "Measurement error: ERR",
        2: "Measurement error: NC or LoC",
        3: "Measurement error: Other errors"
    }

    def __init__(self, name, address, **kwargs):
        """
        Initializes an instance of the ZM2376 class.

        Parameters:
            name (str): Name of the instrument.
            address (str): Address of the instrument.
            **kwargs: Additional keyword arguments to be passed to the parent class.

        Returns:
            None.
        """
        super().__init__(name, address, terminator='\r\n', **kwargs)
        self.connect_message()

        self.add_parameter(
            "primary",
            get_cmd=self._get_output,
            get_parser=self._primary_parser,
            set_cmd=":calc1:form {}",
            label="Primary Parameter"
        )

        self.add_parameter(
            "secondary",
            get_cmd=self._get_output,
            get_parser=self._secondary_parser,
            set_cmd=":calc2:form {}",
            label="Secondary Parameter"
        )

        self.add_parameter(
            "frequency",
            get_cmd=":sour:freq?",
            get_parser=float,
            set_cmd=":sour:freq {:f}",
            label="Frequency",
            unit="Hz"
        )

        self.add_parameter(
            "correction_lower_limit",
            get_cmd=":corr:lim:low?",
            get_parser=float,
            set_cmd=":corr:lim:low {}",
            label="Correction Lower Limit Frequency",
            unit="Hz"
        )

        self.add_parameter(
            "correction_upper_limit",
            get_cmd=":corr:lim:upp?",
            get_parser=float,
            set_cmd=":corr:lim:upp {}",
            label="Correction Upper Limit Frequency",
            unit="Hz"
        )

        self.add_parameter(
            "short_correction_state",
            get_cmd=":corr:shor?",
            get_parser=int,
            set_cmd=":corr:shor {}",
            label="Short Correction State"
        )
        
        self.add_parameter(
            "open_correction_state",
            get_cmd=":corr:open?",
            get_parser=int,
            set_cmd=":corr:open {}",
            label="Open Correction State"
        )

        self.add_parameter(
            "load_correction_state",
            get_cmd=":corr:load?",
            get_parser=int,
            set_cmd=":corr:load {}",
            label="Load Correction State"
        )

        self.add_parameter(
            "primary_var",
            get_cmd=":calc1:form?",
            get_parser=str,
            set_cmd=":calc1:form {}",
            label="Primary Parameter Variable"
        )

        self.add_parameter(
            "secondary_var",
            get_cmd=":calc2:form?",
            get_parser=str,
            set_cmd=":calc2:form {}",
            label="Secondary Parameter Variable"
        )

        self.add_parameter(
            "dc_bias",
            get_cmd=":sour:volt:offs?",
            get_parser=float,
            set_cmd=":sour:volt:offs {}",
            label="DC Bias",
            unit="V"
        )

        self.add_parameter(
            "dc_bias_state",
            get_cmd=":sour:volt:offs:stat?",
            get_parser=float,
            set_cmd=":sour:volt:offs:stat {}",
            set_parser=self._state_parser,
            label="DC Bias State",
        )


    def _get_output(self) -> str:
        """
        Helper method to retrieve the measurement output from the instrument.

        Returns:
            output (str): Measurement output as a string.

        Raises:
            RuntimeError: If the measurement status indicates an error.
        """
        output = self.ask(":fetch?")

        if int(output.split(",")[0]) == 0:
            msg = output
        else:
            raise RuntimeError(self.ERROR_STATEMENTS[int(output.split(",")[0])])

        return msg

    def change_correction_limits(self, lower_limit, upper_limit):
        """
        Helper method to change the correction limits.

        Parameters:
            lower_limit (float): Lower limit of the correction frequency.
            upper_limit (float): Upper limit of the correction frequency.

        Returns:
            None.
        """
        self.correction_lower_limit.set(lower_limit)
        self.correction_upper_limit.set(upper_limit)

    def open_correction(self, lower_limit=0.02, upper_limit=5.5e6):
        """
        Performs open circuit correction with the specified lower and upper limits.

        Parameters:
            lower_limit (float): Lower limit of the correction frequency.
            upper_limit (float): Upper limit of the correction frequency.

        Returns:
            None.
        """
        self.change_correction_limits(lower_limit, upper_limit)
        self.write("corr:coll stan1")

    def short_correction(self, lower_limit=0.02, upper_limit=5.5e6):
        """
        Performs short circuit correction with the specified lower and upper limits.

        Parameters:
            lower_limit (float): Lower limit of the correction frequency.
            upper_limit (float): Upper limit of the correction frequency.

        Returns:
            None.
        """
        self.change_correction_limits(lower_limit, upper_limit)
        self.write("corr:coll stan2")

    def load_correction(self):
        """
        Performs load correction.

        Returns:
            None.
        """
        self.write("corr:coll stan3")

    def _primary_parser(self, msg: str):
        """
        Parser method to extract the primary measurement value from the measurement output.

        Parameters:
            msg (str): Measurement output as a string.

        Returns:
            measurement (float): Primary measurement value.
        """
        measurement = [float(x) for x in msg.split(",")]
        return measurement[1]

    def _secondary_parser(self, msg: str):
        """
        Parser method to extract the secondary measurement value from the measurement output.

        Parameters:
            msg (str): Measurement output as a string.

        Returns:
            measurement (float): Secondary measurement value.
        """
        measurement = [float(x) for x in msg.split(",")]
        return measurement[2]

    def _state_parser(self, state: bool):
        """
        Parser method to set the state of any parameter.

        Parameters:
            state (boolean): True or False

        Returns:
            state (str): 0 or 1
        """
        if state:
            return "1"
        else:
            return "0"