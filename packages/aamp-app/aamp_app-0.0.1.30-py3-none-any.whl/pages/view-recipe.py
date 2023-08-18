from dash import Dash, html, dcc, dash_table, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash

dash.register_page(__name__, path="/view-recipe", name="View Recipe", title="View Recipe")

layout = html.Div(
    [
        html.H1("View Recipe"),
        html.Div(
            [
                dbc.Alert(
                    id="view-recipe-alert",
                    color="success",
                    is_open=False,
                    fade=True,
                    className="mb-3",
                ),
                html.Div(
                    [
                        html.H2("Devices"),
                        dbc.ButtonGroup(
                            [
                                dbc.Button("Refresh", id="refresh-button1", n_clicks=0),
                                dbc.Button("Add device", id="add-device-button"),
                                dbc.Button("Edit", id="edit-device-button"),
                                dbc.Button("Delete", id="delete-device-button"),
                            ],
                            className="mb-3",
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Editor"), close_button=False),
                                dbc.ModalBody(
                                    [
                                        dcc.Textarea(
                                            id="device-json-editor",
                                            style={
                                                "width": "100%",
                                                "height": "200px",
                                                "fontFamily": "monospace",
                                                "backgroundColor": "#f5f5f5",
                                                "border": "1px solid #ccc",
                                                "padding": "10px",
                                                "color": "#333",
                                            },
                                        ),
                                        html.Div(
                                            id="edit-device-error",
                                            style={"color": "red"},
                                        ),
                                        html.Div(
                                            id="edit-device-serial-ports-info",
                                        ),
                                    ]
                                ),
                                dbc.ModalFooter(dbc.Button("Save", id="save-device-editor")),
                            ],
                            id="device-editor-modal",
                            keyboard=False,
                            backdrop="static",
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Add Device")),
                                dbc.ModalBody(
                                    [
                                        dcc.Dropdown(
                                            id="add-device-dropdown",
                                            options=[],
                                            value=None,
                                            className="mb-2",
                                        ),
                                        dcc.Textarea(
                                            id="add-device-json-editor",
                                            style={
                                                "width": "100%",
                                                "height": "200px",
                                                "fontFamily": "monospace",
                                                "backgroundColor": "#f5f5f5",
                                                "border": "1px solid #ccc",
                                                "padding": "10px",
                                                "color": "#333",
                                            },
                                        ),
                                        html.Div(
                                            id="add-device-error",
                                            style={"color": "red", "display": "none"},
                                        ),
                                        html.Div(
                                            id="add-device-serial-ports-info",
                                        ),
                                    ]
                                ),
                                dbc.ModalFooter(dbc.Button("Add", id="add-device-editor")),
                            ],
                            id="device-add-modal",
                            keyboard=False,
                            backdrop="static",
                        ),
                        html.Div(
                            children=[dash_table.DataTable(id="devices-table")],
                            id="devices-table-div",
                        ),
                    ],
                    className="table-container mb-3",
                ),
                html.Div(
                    [
                        html.H2("Commands"),
                        dbc.ButtonGroup(
                            [
                                dbc.Button("Refresh", id="refresh-button2", n_clicks=0),
                                dbc.Button("Add command", id="add-command-open-modal-button"),
                                dbc.Button("Edit", id="edit-command-button"),
                                dbc.Button("Delete", id="delete-command-button"),
                            ],
                            className="mb-3",
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Editor"), close_button=False),
                                dbc.ModalBody(
                                    [
                                        dcc.Textarea(
                                            id="command-json-editor",
                                            style={
                                                "width": "100%",
                                                "height": "200px",
                                                "fontFamily": "monospace",
                                                "backgroundColor": "#f5f5f5",
                                                "border": "1px solid #ccc",
                                                "padding": "10px",
                                                "color": "#333",
                                            },
                                        ),
                                        html.Div(
                                            id="edit-command-error",
                                            style={"color": "red"},
                                        ),
                                    ]
                                ),
                                dbc.ModalFooter(dbc.Button("Save", id="save-command-editor")),
                            ],
                            id="command-editor-modal",
                            keyboard=False,
                            backdrop="static",
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Add Command")),
                                dbc.ModalBody(
                                    [
                                        dcc.Dropdown(
                                            id="view-recipe-add-command-device-dropdown",
                                            options=[],
                                            value=None,
                                        ),
                                        dcc.Dropdown(
                                            id="view-recipe-add-command-command-dropdown",
                                            options=[],
                                            value=None,
                                            className="mb-2",
                                        ),
                                        dcc.Textarea(
                                            id="view-recipe-add-command-json-editor",
                                            style={
                                                "width": "100%",
                                                "height": "200px",
                                                "fontFamily": "monospace",
                                                "backgroundColor": "#f5f5f5",
                                                "border": "1px solid #ccc",
                                                "padding": "10px",
                                                "color": "#333",
                                            },
                                        ),
                                        html.Div(
                                            id="add-command-error",
                                            style={"color": "red"},
                                        ),
                                    ]
                                ),
                                dbc.ModalFooter(
                                    dbc.Button("Add", id="view-recipe-add-command-editor")
                                ),
                            ],
                            id="view-recipe-command-add-modal",
                            keyboard=False,
                            backdrop="static",
                        ),
                        html.Div(
                            children=[dash_table.DataTable(id="commands-table")],
                            id="commands-table-div",
                        ),
                        # dbc.Accordion(
                        #     [
                        #         dbc.AccordionItem(
                        #             "item1", title="Item 1", item_id="item1"
                        #         )
                        #     ],
                        #     id="commands-accordion",
                        #     # start_collapsed=True,
                        #     style={"display": "none"},
                        # ),
                    ],
                    className="table-container mb-3",
                ),
                html.Div(
                    [
                        html.H2("Execution Options"),
                        dbc.Row(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H5("Default Execution Record Name"),
                                                dbc.Col(
                                                    [
                                                        dbc.Input(
                                                            id="view-recipe-execution-options-default-execution-record-name",
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                html.H5("Output Files"),
                                                dbc.Textarea(
                                                    id="view-recipe-execution-options-output-files",
                                                    placeholder="Enter one filename with extension per line",
                                                ),
                                            ]
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                            ]
                        ),
                        dbc.Button(
                            "Save Options",
                            id="view-recipe-execution-options-save-button",
                            n_clicks=0,
                            className="mb-3",
                        ),
                        dbc.Label(
                            "Execution Options Saved",
                            id="view-recipe-execution-options-saved-label",
                            style={"display": "none"},
                        ),
                    ],
                    className="table-container mb-5",
                )
                # html.Div(
                #     [
                #         html.H2("Command Iterations"),
                #         html.Button("Refresh", id="refresh-button3", n_clicks=0),
                #         html.Div(id="table-container3"),
                #     ],
                #     className="table-container",
                # ),
            ],
            className="tables-container",
        ),
    ],
    className="container",
)


@callback(
    Output("device-editor-modal", "is_open"),
    [Input("edit-device-button", "n_clicks"), Input("save-device-editor", "n_clicks")],
    [State("device-editor-modal", "is_open")],
)
def toggle_device_editor_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@callback(
    Output("device-add-modal", "is_open"),
    [Input("add-device-button", "n_clicks"), Input("add-device-editor", "n_clicks")],
    [State("device-add-modal", "is_open")],
)
def toggle_device_add_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@callback(
    Output("command-editor-modal", "is_open"),
    [
        Input("edit-command-button", "n_clicks"),
        Input("save-command-editor", "n_clicks"),
    ],
    [State("command-editor-modal", "is_open")],
)
def toggle_command_editor_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
