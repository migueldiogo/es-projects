var { Router,
      Route,
      IndexRoute,
      IndexLink,
      hashHistory,
      Link } = ReactRouter;

class App extends React.Component{
    render(){
        return(
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


class Login extends React.Component{
    render(){
        return(
            <div id="login">
                <h2>Login</h2>
                <form id="login_form">
                    <div className="form-group">
                        <h4>Email:</h4>
                        <input type="email" className="form-control" id="login_email" placeholder="Enter email"/>
                    </div>
                    <div className="form-group">
                        <h4>Password:</h4>
                        <input type="password" className="form-control" id="login_password" placeholder="Enter password"/>
                    </div>
                        <button type="submit" className="btn btn-default">Submit</button>
                </form>
            </div>
        );
    }
}

class Register extends React.Component{
    submitRegister(){

    }

    render(){
        return (
            <div id="register">
                <h2>Register Account</h2>
                <form id="register_form" ref="r_form" onSubmit={this.submitRegister.bind(this)} action="http://127.0.0.1:5000/api/v1/users/" method="POST">
                    <div className="form-group">
                        <h4>First Name:</h4>
                        <input type="text" className="form-control" id="firstName" required name="firstName" placeholder="Enter your first name"/>
                    </div>
                    <div className="form-group">
                        <h4>Last Name:</h4>
                        <input type="text" className="form-control" id="lastName" required name="lastName" placeholder="Enter your last name"/>
                    </div>
                    <div className="form-group">
                        <h4>Email:</h4>
                        <input ref="mail" type="email" className="form-control" id="email" required name="email" placeholder="Enter email"/>
                    </div>
                    <div className="form-group">
                        <h4>Password:</h4>
                        <input type="password" className="form-control" id="password" required name="password" placeholder="Enter password"/>
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
            <IndexRoute component={Login} />
            <Route path="register" component={Register}/>
        </ReactRouter.Route>
    </ReactRouter.Router>,
    container);