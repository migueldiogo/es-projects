var {
    Router,
    Route,
    IndexRoute,
    IndexLink,
    hashHistory,
    Link
} = ReactRouter;

class App extends React.Component {
    render() {
        return (
            <div>
                <h1>Welcome to SoundShare!</h1>
                <ul className="header">
                    <li><IndexLink to="/" activeClassName="active">Login</IndexLink></li>
                    <li><Link to="/register" activeClassName="active">Register Account</Link></li>
                </ul>
                <div className="content">
                    {this.props.children}
                </div>
            </div>
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
        else{
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
                .then(response=>{
                    if (response.status==401){
                        alert("Invalid credentials!");
                        return;
                    }
                    else if (response.status!=200){
                        alert("Could not do login.");
                        return;
                    }
                    response.json()
                        .then(json=>{
                            alert("Login successful!");
                            localStorage.setItem("token", json.token);
                            console.log(localStorage.getItem("token"));
                        });
                });

        }
        event.preventDefault();
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
        event.preventDefault();
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


ReactDOM.render(
    <ReactRouter.Router history={ReactRouter.hashHistory}>
        <ReactRouter.Route path="/" component={App}>
            <IndexRoute component={Login}/>
            <Route path="register" component={Register}/>
        </ReactRouter.Route>
    </ReactRouter.Router>,
    container);