# Author: Davis Thomas Daniel
# Project: droic
# Module: ui.callbacks

import time
import logging
import dash
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from dash import html

# from droic
from utils.adb import get_device_model, get_unique_devices
from utils.manager import NotificationManager


def register_callbacks(
    app, connection_manager, monitoring_state, monitoring_controller
):
    """Register all callbacks for the droidetric dashboard"""
    
    # start a notification manager initially
    notification_manager = NotificationManager()

    @app.callback(
        Output("connection-status", "children"),
        Output("connection-status", "className"),
        [
            Input("device-check-interval", "n_intervals"),
            Input("refresh-button", "n_clicks"),
        ],
    )
    def check_device_availability(_, refresh_clicks):
        """Check if devices are available and udate status in device-status-box"""

        unique_devices = get_unique_devices()

        # check if it was refresh button that triggered the callback and log
        trigger_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        if trigger_id == "refresh-button" and refresh_clicks:
            logging.info("Manual refresh of device list triggered.")
            logging.info(f"Found following devices: {unique_devices}")
            notification_manager.set_notification(
                "Refreshed device list.", "notification-success", priority=3
            )
            if unique_devices:
                time.sleep(1)
                notification_manager.clear_notification()
                notification_manager.set_notification(
                "Found devices.", "notification-success", priority=3
                )
                logging.info(f"Found following devices: {unique_devices}")
            else:
                time.sleep(1)
                notification_manager.clear_notification()
                notification_manager.set_notification(
                "Found no devices.", "notification-error", priority=3
                )
                logging.warning("No devices found.")

        if unique_devices:
            status_text = [
                html.Div(
                    "Devices are available.",
                    style={
                        "marginTop": "0",
                        "marginBottom": "10px",
                        "textAlign": "center",
                    },
                )
            ]

            device_list = []  # device_list 
            for serial_number, device_ids in unique_devices.items():
                # check for unqiue devices based on serial numbers
                usb_found = any(":" not in dev_id for dev_id in device_ids)
                wifi_found = any(":" in dev_id for dev_id in device_ids)

            
                device_id = next((d for d in device_ids if ":" not in d), device_ids[0])
                model = get_device_model(device_id)

                # create a pill-holder for each device
                device_pill = html.Div(
                    [
                        html.Div(
                            [
                                # device model name
                                html.Span(
                                    model,
                                    className="pill-title",
                                    style={"fontWeight": "bold", "fontSize": "16px"},
                                ),
                                # connection : wifi or usb
                                html.Div(
                                    [
                                        html.Span(
                                            "USB" if usb_found else "",
                                            className="conn-usb"
                                            if usb_found
                                            else "pill-hidden",
                                        ),
                                        html.Span(
                                            "Wi-Fi" if wifi_found else "",
                                            className="conn-wifi"
                                            if wifi_found
                                            else "pill-hidden",
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "gap": "5px",
                                    },
                                ),
                            ],
                            className="status-pill",
                        )
                    ],
                    style={
                        "marginBottom": "10px",
                        "display": "inline-block",
                        "marginRight": "10px"
                    },
                )

                device_list.append(device_pill)

            status_text.append(
                html.Div(
                    device_list,
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "justifyContent": "flex-start",
                        "gap": "10px",
                        "maxWidth": "1000px"
                    },
                )
            )

            return status_text, "device-status-box device-status-success"

        else:
            no_device_text = html.Div(
                "No devices available. Connect a device via USB or Wi-Fi.",
                style={"marginTop": "0", "marginBottom": "0px", "textAlign": "center"},
            )
            return no_device_text, "device-status-box device-status-error"

    @app.callback(
        Output("device-dropdown", "options"),
        [
            Input("device-check-interval", "n_intervals"),
            Input("refresh-button", "n_clicks"),
        ],
    )
    def update_device_dropdown(_, refresh_clicks):
        """Update the device dropdown list with available devices"""
        # get unique devices first.
        unique_devices = get_unique_devices()
        options = []

        for serial_number, device_ids in unique_devices.items():
            model = get_device_model(device_ids[0])
            usb_available = any(":" not in dev_id for dev_id in device_ids)
            wifi_available = any(":" in dev_id for dev_id in device_ids)

            # connection type indicators
            conn_types = []
            if usb_available:
                conn_types.append("USB")
            if wifi_available:
                conn_types.append("Wi-Fi")

            conn_type_str = " & ".join(conn_types)

            # don't remove serial_number from the option text, this is parsed by wifi_connect!
            # improve logic later
            option_text = f"{model} - Serial: {serial_number} ({conn_type_str})"
            options.append({"label": option_text, "value": f"serial:{serial_number}"})
        
        return options

    @app.callback(
        [Output("device-info", "children"), Output("auto-stopped-state", "children")],
        Input("device-check-interval", "n_intervals"),
    )
    def update_device_and_auto_stopped(_):
        """Update the device info box and auto-stopped state"""

        auto_stopped_state = str(monitoring_state.auto_stopped)

        device_info_ui = html.Div(
            "No device is being monitored.",
            style={"marginTop": "0", "marginBottom": "10px", "textAlign": "center"},
            className="device-info-box device-info-empty",
        )

        if monitoring_state.monitoring_active:
            if monitoring_state.monitoring_paused:
                time_elapsed = 0
                time_remaining = monitoring_state.max_pause_duration
                if monitoring_state.pause_start_time:
                    time_elapsed = int(time.time() - monitoring_state.pause_start_time)
                    time_remaining = max(
                        0, monitoring_state.max_pause_duration - time_elapsed
                    )
                device_info_ui = html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span("Status", className="pill-title"),
                                        html.Span(
                                            "Waiting",
                                            className="pill-value monitoring-status-paused",
                                        ),
                                    ],
                                    className="status-pill",
                                ),
                                html.Div(
                                    [
                                        html.Span("Device", className="pill-title"),
                                        html.Span(
                                            f"{connection_manager.device_info['model']} ({connection_manager.device_info['persistent_id']})",
                                            className="pill-value",
                                        ),
                                    ],
                                    className="status-pill",
                                ),
                                html.Div(
                                    [
                                        html.Span("Timeout", className="pill-title"),
                                        html.Span(
                                            f"{time_remaining}s",
                                            className="pill-value monitoring-status-paused",
                                        ),
                                    ],
                                    className="status-pill",
                                ),
                                html.Div(
                                    [
                                        html.Span(
                                            "Data Points", className="pill-title"
                                        ),
                                        html.Span(
                                            str(monitoring_state.total_points),
                                            className="pill-value",
                                        ),
                                    ],
                                    className="status-pill",
                                ),
                            ],
                            className="pill-row",
                        )
                    ],
                    className="device-info-box device-info-reconnecting",
                )

            # normal active monitoring state
            elif connection_manager.device_info["device_id"]:
                current_connection_type = (
                    "Wi-Fi"
                    if ":" in connection_manager.device_info["device_id"]
                    else "USB"
                )
                # update stored connection type if it has changed
                if (
                    current_connection_type
                    != connection_manager.device_info["connection_type"]
                ):
                    connection_manager.device_info["connection_type"] = (
                        current_connection_type
                    )

                device_info_ui = html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span("Status", className="pill-title"),
                                        html.Span(
                                            "Active",
                                            className="pill-value monitoring-status-active",
                                        ),
                                    ],
                                    className="status-pill",
                                ),
                                html.Div(
                                    [
                                        html.Span("Device", className="pill-title"),
                                        html.Span(
                                            f"{connection_manager.device_info['model']} ({connection_manager.device_info['persistent_id']})",
                                            className="pill-value",
                                        ),
                                    ],
                                    className="status-pill",
                                ),
                                html.Div(
                                    [
                                        html.Span("Connection", className="pill-title"),
                                        html.Span(
                                            current_connection_type,
                                            className="pill-value conn-wifi"
                                            if current_connection_type == "Wi-Fi"
                                            else "pill-value conn-usb",
                                        ),
                                    ],
                                    className="status-pill",
                                ),
                                html.Div(
                                    [
                                        html.Span("Storage", className="pill-title"),
                                        html.Span(
                                            "Active"
                                            if monitoring_state.save_to_local_db
                                            else "Inactive",
                                            className="pill-value monitoring-status-active"
                                            if monitoring_state.save_to_local_db
                                            else "pill-value monitoring-status-inactive",
                                        ),
                                    ],
                                    className="status-pill",
                                ),
                                html.Div(
                                    [
                                        html.Span(
                                            "Data Points", className="pill-title"
                                        ),
                                        html.Span(
                                            str(monitoring_state.total_points),
                                            className="pill-value",
                                        ),
                                    ],
                                    className="status-pill",
                                ),
                            ],
                            className="pill-row",
                        )
                    ],
                    className="device-info-box",
                )
            else:
                device_info_ui = html.Div(
                    "Device connection lost. Attempting to reconnect...",
                    className="device-info-box device-info-error",
                )

        return device_info_ui, auto_stopped_state

    @app.callback(Input("clear-button", "n_clicks"), prevent_initial_call=True)
    def clear_data(n_clicks):
        """Clear data button callback"""
        if n_clicks>0:
            logging.info("Clear data button clicked.")
            # also tries to clear notifications.
            notification_manager.clear_notification()
            # also handle clear data functionality
            if len(monitoring_state.collected_data) == 0:
                logging.warning("No data to clear.")
                notification_manager.set_notification(
                    "No data to clear.", "notification-error", priority=3
                )
            else:
                monitoring_state.collected_data.drop(
                    monitoring_state.collected_data.index, inplace=True
                )
                monitoring_state.total_points = 0
                logging.info("Data cleared.")
                notification_manager.set_notification(
                    "Data cleared.", "notification-success", priority=3
                )
            
    @app.callback(Input("save-to-db-dropdown", "value"))
    def handle_save_to_db(save_value):
        """Handle save to DB dropdown changes"""

        monitoring_state.save_to_local_db = save_value == "save"
        msg = (
            "Saving to local database is enabled."
            if monitoring_state.save_to_local_db
            else "Saving to local database is disabled."
        )

        notification_manager.set_notification(
            msg,
            "notification-success"
            if monitoring_state.save_to_local_db
            else "notification-error",
            priority=3,
        )

    @app.callback([Input("wifi-connect-button", "n_clicks")],[State("device-dropdown", "value")])
    def handle_wifi_connect(n_clicks,selected_device):
        """Handle Wi-Fi connect button clicks"""
        if n_clicks > 0:
            logging.info("Wi-Fi connect button clicked.")
            # check if a device is selected
            if not selected_device:
                logging.error("No device was selected for initiating Wi-Fi connection.")
                notification_manager.set_notification(
                    "No device selected. Please select a device first.",
                    "notification-error",
                    priority=5,
                )
            else:
                # check if device is already connected via Wi-Fi
                serial_number = selected_device.split("serial:")[1]
                current_devices = get_unique_devices()
                if len(current_devices[serial_number])>0:
                    logging.info("Found USB connection of device, trying to connect via Wi-Fi")
                    success, message = connection_manager.try_wifi_connect(serial_number)
                    class_name = "notification-success" if success else "notification-error"
                    notification_manager.set_notification(message, class_name, priority=5)
                else:
                    logging.info("No USB connection was found for selected device.")
                    notification_manager.set_notification("Device must be connected via USB first.","notification-error",priority=5)


    @app.callback(
        Output("general-notification", "children"),
        Output("general-notification", "className"),
        Output("notification-clear-interval", "disabled"),
        [
            Input("interval-component", "n_intervals"),
            Input("notification-clear-interval", "n_intervals"),
        ],prevent_initial_call=True,
    )
    def notification_handler(
        interval_check,
        notification_clear_interval,
    ):
        """handler for all notification-related events"""


        ctx = dash.callback_context
        if not ctx.triggered:

            return "", "notification-hidden", True, False

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "notification-clear-interval":
            current_time = time.time()
            if current_time > notification_manager.expiry_time:
                notification_manager.clear_notification()

        message, class_name, clear_disabled = (
            notification_manager.get_notification_state()
        )
        return message, class_name, clear_disabled

    @app.callback(
        Output("droic-plot", "figure"),
        [Input("interval-component", "n_intervals"),
        Input("stop-button", "n_clicks"),
        Input("metric-selector-dropdown", "value"),
        Input("specific-metrics-dropdown", "value")],
        [State("droic-plot", "figure"),
        State("available-metrics-store", "data")]
    )
    def update_graph(_, stop_clicks, metric, selected_metrics, current_fig, available_metrics):
        fig = go.Figure()

        if not hasattr(monitoring_state, "last_metric"):
            monitoring_state.last_metric = metric
        
        if not hasattr(monitoring_state, "last_specific_metrics"):
            monitoring_state.last_specific_metrics = selected_metrics

        metric_changed = monitoring_state.last_metric != metric
        specific_metrics_changed = monitoring_state.last_specific_metrics != selected_metrics
        
        if metric_changed:
            monitoring_state.last_metric = metric
        
        if specific_metrics_changed:
            monitoring_state.last_specific_metrics = selected_metrics

        if metric == "cpu":
            all_metrics = [
                "cpu_cpu",
                "cpu_user",
                "cpu_nice",
                "cpu_sys",
                "cpu_idle",
                "cpu_iow",
                "cpu_irq",
                "cpu_sirq",
                "cpu_host",
            ]
            max_default = 100
        elif metric == "mem":
            all_metrics = [
                "mem_total",
                "mem_used",
                "mem_free",
                "mem_buffers",
                "swap_total",
                "swap_used",
                "swap_free",
                "swap_cached",
            ]
            max_default = 5633892
        elif metric == "tasks":
            all_metrics = [
                "tasks_total",
                "tasks_running",
                "tasks_sleeping",
                "tasks_stopped",
                "tasks_zombie",
            ]
            max_default = 100 
        else:
            all_metrics = []
            max_default = 100
        
        if selected_metrics and len(selected_metrics) > 0:
            metrics = [m for m in all_metrics if m in selected_metrics]
        else:
            metrics = all_metrics


        if not monitoring_state.collected_data.empty:

            for m in metrics:
                if m in monitoring_state.collected_data.columns:

                    if m.startswith("cpu_"):
                        display_name = m.replace("cpu_", "").capitalize()
                    elif m.startswith("mem_"):
                        display_name = m.replace("mem_", "").capitalize()
                    elif m.startswith("swap_"):
                        display_name = m.replace("swap_", "Swap ").capitalize()
                    elif m.startswith("tasks_"):
                        display_name = m.replace("tasks_", "").capitalize()
                    else:
                        display_name = m.capitalize()

                    fig.add_trace(
                        go.Scatter(
                            x=monitoring_state.collected_data["timestamp"],
                            y=monitoring_state.collected_data[m],
                            mode="lines+markers",
                            name=display_name,
                        )
                    )


        y_axis_labels = {
            "cpu": "CPU Usage (%)",
            "mem": "Memory (MB)",
            "tasks": "Number of Tasks",
        }


        if not monitoring_state.collected_data.empty:
            valid_metrics = [
                m for m in metrics if m in monitoring_state.collected_data.columns
            ]
            if valid_metrics:
                calculated_max = (
                    monitoring_state.collected_data[valid_metrics].max().max() * 1.1
                )
                y_max = max(calculated_max, max_default)
            else:
                y_max = max_default
        else:
            y_max = max_default


        fig.update_layout(
            title="",
            xaxis_title="Time",
            yaxis_title=y_axis_labels.get(metric, "Value"),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            margin=dict(l=40, r=40, t=50, b=40),
            hovermode="closest",
            template="plotly_white",
        )


        if metric_changed or specific_metrics_changed:
            fig.update_layout(
                yaxis=dict(range=[0, y_max], autorange=True), 
                xaxis=dict(autorange=True)
            )

        elif monitoring_state.monitoring_active:
            fig.update_layout(
                yaxis=dict(
                    range=[0, y_max],
                    autorange=True,
                    fixedrange=True,  
                ),
                xaxis=dict(
                    autorange=True,
                    fixedrange=True, 
                ),
            )
        else:

            if current_fig and "layout" in current_fig:
                try:
                    xaxis_range = current_fig["layout"]["xaxis"]["range"]
                    yaxis_range = current_fig["layout"]["yaxis"]["range"]
                except (KeyError, TypeError):
                    if not monitoring_state.collected_data.empty:
                        xaxis_range = [
                            monitoring_state.collected_data["timestamp"].min(),
                            monitoring_state.collected_data["timestamp"].max(),
                        ]
                        yaxis_range = [0, y_max]
                    else:
                        xaxis_range = None
                        yaxis_range = [0, y_max]
            else:
                if not monitoring_state.collected_data.empty:
                    xaxis_range = [
                        monitoring_state.collected_data["timestamp"].min(),
                        monitoring_state.collected_data["timestamp"].max(),
                    ]
                    yaxis_range = [0, y_max]
                else:
                    xaxis_range = None
                    yaxis_range = [0, y_max]

            fig.update_layout(
                yaxis=dict(
                    autorange=False,
                    range=yaxis_range,
                    fixedrange=False,  
                ),
                xaxis=dict(
                    autorange=False if xaxis_range else True,
                    range=xaxis_range if xaxis_range else None,
                    fixedrange=False,
                ),
            )

        return fig


    @app.callback(
        [Output("specific-metrics-dropdown", "options"),
        Output("specific-metrics-dropdown", "value"),
        Output("available-metrics-store", "data")],
        [Input("metric-selector-dropdown", "value")]
    )
    def update_specific_metrics_options(metric_category):
        """Update the specific metrics dropdown options based on the selected category."""
        if metric_category == "cpu":
            metrics = [
                {"label": "CPU Overall", "value": "cpu_cpu"},
                {"label": "User", "value": "cpu_user"},
                {"label": "Nice", "value": "cpu_nice"},
                {"label": "System", "value": "cpu_sys"},
                {"label": "Idle", "value": "cpu_idle"},
                {"label": "I/O Wait", "value": "cpu_iow"},
                {"label": "IRQ", "value": "cpu_irq"},
                {"label": "Soft IRQ", "value": "cpu_sirq"},
                {"label": "Host", "value": "cpu_host"},
            ]
        elif metric_category == "mem":
            metrics = [
                {"label": "Total Memory", "value": "mem_total"},
                {"label": "Used Memory", "value": "mem_used"},
                {"label": "Free Memory", "value": "mem_free"},
                {"label": "Buffers", "value": "mem_buffers"},
                {"label": "Swap Total", "value": "swap_total"},
                {"label": "Swap Used", "value": "swap_used"},
                {"label": "Swap Free", "value": "swap_free"},
                {"label": "Swap Cached", "value": "swap_cached"},
            ]
        elif metric_category == "tasks":
            metrics = [
                {"label": "Total Tasks", "value": "tasks_total"},
                {"label": "Running Tasks", "value": "tasks_running"},
                {"label": "Sleeping Tasks", "value": "tasks_sleeping"},
                {"label": "Stopped Tasks", "value": "tasks_stopped"},
                {"label": "Zombie Tasks", "value": "tasks_zombie"},
            ]
        else:
            metrics = []
        
        metric_values = [m["value"] for m in metrics]
        
        return metrics, [], metric_values

    @app.callback(
        Output("start-button", "disabled"),
        Output("stop-button", "disabled"),
        Output("device-dropdown", "disabled"),
        Output("interval-input", "disabled"),
        Output("refresh-button", "disabled"),
        Output("save-to-db-dropdown", "disabled"),
        Output("device-dropdown", "value"),
        [
            Input("start-button", "n_clicks"),
            Input("stop-button", "n_clicks"),
            Input("device-check-interval", "n_intervals"),
        ],
        [State("interval-input", "value"), State("device-dropdown", "value")],
        prevent_initial_call=True,
    )
    def manage_monitoring(
        start_clicks, stop_clicks, n_intervals, interval_value, selected_device
    ):
        ctx = dash.callback_context
        trigger_id = (
            ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
        )
        
        if monitoring_state.auto_stopped:
            logging.info("Auto-stopped state detected.")
            monitoring_state.auto_stopped = False
            return False, True, False, False, False, False, selected_device
        

        if selected_device is None:

            unique_devices = get_unique_devices()
            if unique_devices:

                first_serial = next(iter(unique_devices))
                logging.info(f"No device specified, auto-selecting first available device: {first_serial}")

                first_device_value = f"serial:{first_serial}"
                logging.info(f"Auto-selected device value: {first_device_value}")
                selected_device = first_device_value
        
        if trigger_id == "device-dropdown" and monitoring_state.monitoring_active:
            # a change occured in device-dropdown while monitoring was active
            # most likely, device lost connection, since device controls are disabled during monitoring
            if selected_device is None:
                logging.critical("Lost connection while monitoring.")
                monitoring_state.monitoring_paused = True


        if trigger_id == "start-button" and start_clicks > 0:
            if not monitoring_state.monitoring_active:
                try:
                    logging.info("Start Button clicked. Initiate monitoring...")
                    monitoring_state.current_device = selected_device
                    logging.info(f"Device which is selected for monitoring is : {monitoring_state.current_device}")
                    success = monitoring_controller.start_monitoring(
                        interval=interval_value, selected_device_id=selected_device
                    )
                    logging.info(f"Monitoring started: {success}")
                except Exception as e:
                    logging.error(f"Error starting monitoring: {e}")
                logging.info(
                    f"Monitoring start {'successful' if success else 'failed'}"
                )

                return True, False, True, True, True, True, selected_device
        
        elif trigger_id == "stop-button" and stop_clicks > 0:
            if monitoring_state.monitoring_active:
                monitoring_controller.stop_monitoring()

                return False, True, False, False, False, False, selected_device
        

        return (
            monitoring_state.monitoring_active,
            not monitoring_state.monitoring_active,
            monitoring_state.monitoring_active,
            monitoring_state.monitoring_active,
            monitoring_state.monitoring_active,
            monitoring_state.monitoring_active,
            selected_device,
        )
    return notification_manager