var {
    Router,
    Route,
    IndexRoute,
    IndexLink,
    hashHistory,
    Link
} = ReactRouter;

class App extends React.Component {
    constructor() {
        super();
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {
            return (
                <div>
                    <h1>Soundshare Menu</h1>
                    <ul className="header">
                        <li><Link to="/updateUser" activeClassName="active">Update User Information</Link></li>
                        <li><Link to="/logout" activeClassName="active">Logout</Link></li>
                    </ul>
                    <div className="content">
                        {this.props.children}
                    </div>
                </div>
            );
        }
        else {
            return (
                <div>
                    <h1>Welcome to SoundShare!</h1>
                    <ul className="header">
                        <li><Link to="/login" activeClassName="active">Login</Link></li>
                        <li><Link to="/register" activeClassName="active">Register Account</Link></li>
                    </ul>
                    <div className="content">
                        {this.props.children}
                    </div>
                </div>
            );
        }
    }

    render() {
        return (
            this.checkCookie()
        );
    }
}


class Login extends React.Component {
    constructor() {
        super();
    }

    handleSubmit(event) {
        if (this.refs.email.value == "" || this.refs.password.value == "") {
            alert("Please fill all the fields.");
        }
        else {
            fetch("http://127.0.0.1:5000/api/v1/users/self/tokens/", {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: this.refs.email.value,
                    password: this.refs.password.value,
                })
            })
                .then(response => {
                    if (response.status == 401) {
                        alert("Invalid credentials!");
                        return;
                    }
                    else if (response.status != 200) {
                        alert("Could not do login.");
                        return;
                    }
                    response.json()
                        .then(json => {
                            alert("Login successful!");
                            localStorage.setItem("token", json.token);
                            console.log(localStorage.getItem("token"));
                            window.location.reload();
                        });
                });

        }
    }

    render() {
        return (
            <div id="login">
                <h2>Login</h2>
                <form id="login_form" onSubmit={this.handleSubmit.bind(this)}>
                    <div className="form-group">
                        <h4>Email:</h4>
                        <input type="email" className="form-control" ref="email" placeholder="Enter email"/>
                    </div>
                    <div className="form-group">
                        <h4>Password:</h4>
                        <input type="password" className="form-control" ref="password" placeholder="Enter password"/>
                    </div>
                    <button type="submit" className="btn btn-default">Submit</button>
                </form>
            </div>
        );
    }
}

class Register extends React.Component {
    constructor() {
        super();
    }

    handleSubmit(event) {
        if (this.refs.firstName.value == "" || this.refs.lastName.value == "" || this.refs.email.value == "" || this.refs.password.value == "") {
            alert("Please fill all the fields.");
        }
        else {
            fetch("http://127.0.0.1:5000/api/v1/users/", {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    firstName: this.refs.firstName.value,
                    lastName: this.refs.lastName.value,
                    email: this.refs.email.value,
                    password: this.refs.password.value,
                })
            })
                .then(response => response.status)
                .then(code => {
                    if (code == 200) {
                        alert("Registration made with success!");
                    }
                    else if (code == 409) {
                        alert("There is already an user with this email");
                    }
                    else {
                        alert("Could not make registration");
                    }
                });
        }
    }

    render() {
        return (
            <div id="register">
                <h2>Register Account</h2>
                <form id="register_form" onSubmit={this.handleSubmit.bind(this)}>
                    <div className="form-group">
                        <h4>First Name:</h4>
                        <input type="text" className="form-control" ref="firstName"
                               placeholder="Enter your first name"/>
                    </div>
                    <div className="form-group">
                        <h4>Last Name:</h4>
                        <input type="text" className="form-control" ref="lastName" placeholder="Enter your last name"/>
                    </div>
                    <div className="form-group">
                        <h4>Email:</h4>
                        <input type="email" className="form-control" ref="email" placeholder="Enter email"/>
                    </div>
                    <div className="form-group">
                        <h4>Password:</h4>
                        <input type="password" className="form-control" ref="password" placeholder="Enter password"/>
                    </div>
                    <button type="submit" className="btn btn-default">Submit</button>
                </form>
            </div>
        );
    }
}

class Logout extends React.Component {
    constructor() {
        super();
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {
            return (
                <div id="logout">
                    <h2>Do you want to logout?</h2>
                    <button className="btn btn-default" onClick={this.handleClick.bind(this)}>Logout</button>
                </div>
            );
        }
        else {
            return (
                <h2>Login to access this feature!</h2>
            );
        }
    }

    handleClick(event) {
        localStorage.removeItem("token");
        window.location.reload();
    }

    render() {
        return (
            this.checkCookie()
        );
    }
}

class UpdateUser extends React.Component {
    constructor() {
        super();
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {
            return (
                <div id="update_user">
                    <h2>Update User Information</h2>
                    <form id="update_user_form" onSubmit={this.handleSubmit.bind(this)}>
                        <div className="form-group">
                            <h4>First Name:</h4>
                            <input type="text" className="form-control" ref="firstName"
                                   placeholder="Enter your first name"/>
                        </div>
                        <div className="form-group">
                            <h4>Last Name:</h4>
                            <input type="text" className="form-control" ref="lastName"
                                   placeholder="Enter your last name"/>
                        </div>
                        <div className="form-group">
                            <h4>Password:</h4>
                            <input type="password" className="form-control" ref="password"
                                   placeholder="Enter password"/>
                        </div>
                        <button type="submit" className="btn btn-default">Submit</button>
                    </form>
                </div>
            );
        }
        else {
            return (
                <h2>Login to access this feature!</h2>
            );
        }
    }

    handleSubmit(event) {
        fetch("http://127.0.0.1:5000/api/v1/users/self/", {
            method: "POST",
            headers: {
                "Authorization": localStorage.getItem("token"),
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                firstName: this.refs.firstName.value,
                lastName: this.refs.lastName.value,
                password: this.refs.password.value,
            })
        })
            .then(response => response.status)
            .then(code => {
                if (code == 200) {
                    alert("User information updated!");
                }
                else {
                    alert("Could not update information");
                }
            });
    }

    render() {
        return (
            this.checkCookie()
        );
    }
}


ReactDOM.render(
    <ReactRouter.Router history={ReactRouter.hashHistory}>
        <ReactRouter.Route path="/" component={App}>
            <Route path="login" component={Login}/>
            <Route path="register" component={Register}/>
            <Route path="logout" component={Logout}/>
            <Route path="updateUser" component={UpdateUser}/>
        </ReactRouter.Route>
    </ReactRouter.Router>,
    container);