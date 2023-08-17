try:
    import logging
    import os
    from applicationinsights.logging import enable
    from applicationinsights import channel
    from applicationinsights import TelemetryClient
    import datetime
    
except BaseException as e:
  print("app_insights_logger Error:", e)

class telemetrylogger:

  def __init__(self,appinsightsId,appinsightsKey,aml_ws,experiment_name,pipeline_id):
    self.appinsightsId = appinsightsId
    self.appinsightsKey = appinsightsKey
    self.aml_ws = aml_ws
    self.experiment_name = experiment_name
    self.pipeline_id = pipeline_id

  def NewTelemetryClient(self):
    try:
      """
          Creates a new Telemetry Client for AML Pipeline 

      Args:
        aml_ws: AML Workspace Name
        experiment_name: AML Experiment Name
        pipeline_id: Pipeline or Job Run Id (Unique Id on AML-WS for a run)
      Returns:
        telemetryClient: telemetry client
      """
      telemetryClient = TelemetryClient(self.appinsightsKey)

      print("Device Type is set to AML Workspace Name: {0} ".format(self.aml_ws))
      print("Device Id is set to AML Experiment Name: {0} ".format(self.experiment_name))
      print("Operation Id is set to Pipeline Run Id: {0} ".format(self.pipeline_id))

      telemetryClient.context.device.type = self.aml_ws
      telemetryClient.context.device.id = self.experiment_name
      telemetryClient.context.operation.id = self.pipeline_id

      print("Mteric Client configured for: AML Workspace Name -> {0},\
       Experiment -> {1},\
        Pipeline Run Id --> {2}".format(self.aml_ws, self.experiment_name, self.pipeline_id))
      return telemetryClient
    except BaseException as e:
      print("app_insights_logger Error:", e)

  def NewAppInsightsClient(self):
    try:
      """
          Creates a new Telemetry Client 

      Args:
        aml_ws: AML Workspace Name
        experiment_name: AML Experiment Name
        pipeline_id: Pipeline or Job Run Id (Unique Id on AML-WS for a run)
      Returns:
        telemetryClient: telemetry client

      """
      if 'APP_INSIGHTS_CLIENT' in locals():
          print("Logging to Application Insights is already configured.")
      else:
          print("Configuring logging to Application Insights")
          APP_INSIGHTS_HANDLER = enable(self.appinsightsKey)
          APP_INSIGHTS_HANDLER.client.context.device.type = self.aml_ws    
          APP_INSIGHTS_HANDLER.client.context.device.id = self.experiment_name
          APP_INSIGHTS_HANDLER.client.context.operation.id = self.pipeline_id      
          APP_INSIGHTS_CLIENT = APP_INSIGHTS_HANDLER.client

          detail_logging = False

          if detail_logging:
            logging.getLogger().setLevel(logging.INFO)
            logging.info("Changed Root logging level set to: %d (%s)", logging.getLogger().level, logging.getLevelName(logging.getLogger().level))

          print("Logging to Application Insights configuration is complete.")
          return APP_INSIGHTS_CLIENT
    except BaseException as e:
      print("app_insights_logger Error:", e)

  def trackEvent(self,telemetryClient, operationName, eventName, properties=None, measurements=None):
    try:
        """ 
            Tracks an event 

        Args:
          telemetryClient: 
          operationName: 
          eventName: 
          properties: custom properties
          measurements: custom measurements
        Returns:
          None

        """
        telemetryClient.context.operation.name = operationName
        telemetryClient.track_event(eventName, properties, measurements)
        telemetryClient.flush()
    except BaseException as e:
      print("app_insights_logger Error:", e)

  def trackTrace(self,APP_INSIGHTS_CLIENT, message, start_date, end_date):
    try:
      """
          Logs an INFO message

      Args:
        message: message to be traced
        start_date: processing start date
        end_date: processing end date
      Returns:
        telemetryClient: None

      """

      APP_INSIGHTS_CLIENT.track_trace(message, {'Incremental Start Date': str(start_date), 'Incremental End Date': str(end_date)}, severity='INFO')
      APP_INSIGHTS_CLIENT.flush()
    except BaseException as e:
      print("app_insights_logger Error:", e)

  def trackException(self,APP_INSIGHTS_CLIENT, exception, start_date, end_date):
    try:
      """ 
          Logs an exception 
      Args:
        exception: exception message
        start_date: processing start date
        end_date: processing end date
      Returns:
        None

      """
      APP_INSIGHTS_CLIENT.track_exception(exception, {'Incremental Start Date': str(start_date), 'Incremental End Date': str(end_date)})
      APP_INSIGHTS_CLIENT.flush()
    except BaseException as e:
      print("app_insights_logger Error:", e)

  def logEvent(self,event_name, properties=None, measurements=None):
    try:
      """ 
          Logs an event using the APP_INSIGHTS_CLIENT
      """
      if 'APP_INSIGHTS_CLIENT' in globals():
        APP_INSIGHTS_CLIENT.track_event(event_name, properties, measurements)
        APP_INSIGHTS_CLIENT.flush()
    except BaseException as e:
      print("app_insights_logger Error:", e)

  def gather_event_details(self,telemetryClient, operationName, eventName, start_date, end_date, source_path, rowCount, event_start_time):
    try:
      """ 
          Gathers event details
      """
      event_end_time = datetime.datetime.now()
      duration = int((event_end_time - event_start_time).total_seconds())
      trackEvent(telemetryClient, operationName, eventName, {'Incremental Start Date': str(start_date), 'Incremental End Date': str(end_date), 'Path': source_path}, {'Record_Count': rowCount, 'Duration': duration, eventName + '_Value': rowCount, eventName + '_Duration': duration})
    except BaseException as e:
      print("app_insights_logger Error:", e)
