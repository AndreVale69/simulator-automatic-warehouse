import dash_bootstrap_components as dbc

GITHUB_PROJECT = "https://github.com/AndreVale69/simulator-automatic-warehouse/"
ICELAB_LINK = "https://www.icelab.di.univr.it/?lang=en"
VERTIMAG_LINK = "https://www.ferrettogroup.com/index.cfm/en/solutions/vertical-storage-system/vertical-lift-module-vertimag/"

navbar = dbc.NavbarSimple(
            [
                dbc.NavItem(dbc.NavLink("Homepage", active=True, href="/")),
                dbc.NavItem(dbc.NavLink("GitHub Project", href=GITHUB_PROJECT, target="_blank")),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("About", header=True),
                        dbc.DropdownMenuItem("IceLab", href=ICELAB_LINK, target="_blank"),
                        dbc.DropdownMenuItem("Vertimag Ferretto Group", href=VERTIMAG_LINK, target="_blank"),
                    ],
                    nav=True, in_navbar=True, label="More"
                )
            ],
            brand="Simulator Automatic Warehouse", brand_href="/", color="dark", dark=True
        )