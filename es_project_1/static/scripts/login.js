var {
    Router,
    Route,
    IndexRoute,
    IndexLink,
    hashHistory,
    Link
} = ReactRouter;

//------------------------ App ------------------------//

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
                        <li className="dropdown"><a>Playlists</a>
                            <ul>
                                <li><Link to="/createPlaylist" activeClassName="active">Create Playlist</Link></li>
                                <li><Link to="/editPlaylist" activeClassName="active">Edit Playlist</Link></li>
                                <li><Link to="/listMyPlaylists" activeClassName="active">List My Playlists</Link></li>
                                <li><Link to="/deletePlaylist" activeClassName="active">Delete Playlist</Link></li>
                            </ul>
                        </li>
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

//------------------------ Login ------------------------//

class Login extends React.Component {
    constructor() {
        super();
    }

    checkCookie() {
        if (localStorage.getItem("token") == null) {
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
                <h2>Choose one of the options above!</h2>
            );
        }
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
            this.checkCookie()
        );
    }
}

//------------------------ Register ------------------------//

class Register extends React.Component {
    constructor() {
        super();
    }

    checkCookie() {
        if (localStorage.getItem("token") == null) {
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
                            <input type="text" className="form-control" ref="lastName"
                                   placeholder="Enter your last name"/>
                        </div>
                        <div className="form-group">
                            <h4>Email:</h4>
                            <input type="email" className="form-control" ref="email" placeholder="Enter email"/>
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
                <h2>Choose one of the options above!</h2>
            );
        }
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
                        window.location.reload();
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
            this.checkCookie()
        );
    }
}

//------------------------ Logout ------------------------//

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
                <h2>Choose one of the options above!</h2>
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

//------------------------ UpdateUser ------------------------//

class UpdateUser extends React.Component {
    constructor() {
        super();
        this.state = {id: 0};
        this.getUserId();
    }

    getUserId() {
        fetch("http://127.0.0.1:5000/api/v1/users/self/", {
            method: "GET",
            headers: {
                "Authorization": localStorage.getItem("token"),
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        })
            .then(response => {
                if (response.status != 200) {
                    return;
                }
                response.json()
                    .then(json => {
                        this.setState({id: json.id});
                    });
            });
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
                <h2>Choose one of the options above!</h2>
            );
        }
    }

    handleSubmit(event) {
        fetch("http://127.0.0.1:5000/api/v1/users/self/" + this.state.id + "/", {
            method: "PUT",
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

//------------------------ CreatePlaylist ------------------------//

class CreatePlaylist extends React.Component {
    constructor() {
        super();
    }

    handleSubmit() {
        if (this.refs.playlistName.value == "") {
            alert("Please fill all the fields.");
        }
        else {
            fetch("http://127.0.0.1:5000/api/v1/playlists/", {
                method: "POST",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name: this.refs.playlistName.value,
                })
            })
                .then(response => response.status)
                .then(code => {
                    if (code == 200) {
                        alert("Playlist successfully created!");
                        window.location.reload();
                    }
                    else {
                        alert("Could not create playlist");
                    }
                });
        }
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {
            return (
                <div id="create_playlist">
                    <h2>Create Playlist</h2>
                    <form id="create_playlist_form" onSubmit={this.handleSubmit.bind(this)}>
                        <div className="form-group">
                            <h4>Playlist Name:</h4>
                            <input type="text" className="form-control" ref="playlistName"
                                   placeholder="Enter name"/>
                        </div>
                        <button type="submit" className="btn btn-default">Submit</button>
                    </form>
                </div>
            );
        }
        else {
            return (
                <h2>Choose one of the options above!</h2>
            );
        }
    }

    render() {
        return (
            this.checkCookie()
        );
    }
}

//------------------------ DeletePlaylist ------------------------//

class DeletePlaylist extends React.Component {
    constructor() {
        super();
        this.state = {selected: 0};
        this.state = {playlists: []};
    }

    componentDidMount() {
        if (localStorage.getItem("token") != null) {
            fetch("http://127.0.0.1:5000/api/v1/users/self/playlists/", {
                method: "GET",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            })
                .then(result => result.json())
                .then(items => this.setState({playlists: items}));
        }
    }


    handleChange(event) {
        this.setState({selected:event.target.value});
    }

    handleClick() {
        if (this.state.selected == 0) {
            alert("Please select a playlist to delete.");
        }
        else{
            fetch("http://127.0.0.1:5000/api/v1/playlists/"+this.state.selected+"/", {
                method: "DELETE",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            })
                .then(response => {
                    if (response.status == 403) {
                        alert("This playlist is not yours!");
                        return;
                    }
                    else if (response.status == 404){
                        alert("Playlist not found.");
                        return;
                    }
                    else if (response.status == 200) {
                        alert("Playlist deleted.");
                        window.location.reload();
                        return;
                    }
                    else{
                        alert("Could not delete playlist.");
                        return;
                    }

                });
        }
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {

            return (
                <div id="delete_playlist">
                    <h2>Select Playlist To Delete</h2>
                    <div>
                        <select onChange={this.handleChange.bind(this)}>
                            <option disabled selected value> -- select an option -- </option>
                            {this.state.playlists.map(playlist => <option value={playlist.id}
                                                                          key={playlist.id}>{playlist.name}</option>)}
                        </select>
                    </div>
                    <button id="delete_playlist" className="btn btn-default" onClick={this.handleClick.bind(this)}>Delete</button>
                </div>
            );
        }
        else {
            return (
                <h2>Choose one of the options above!</h2>
            );
        }
    }

    render() {
        return (
            this.checkCookie()
        );
    }
}

//------------------------ EditPlaylist ------------------------//

class EditPlaylist extends React.Component {
    constructor() {
        super();
        this.state = {selected: 0};
        this.state = {playlists: []};
    }

    componentDidMount() {
        if (localStorage.getItem("token") != null) {
            fetch("http://127.0.0.1:5000/api/v1/users/self/playlists/", {
                method: "GET",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            })
                .then(result => result.json())
                .then(items => this.setState({playlists: items}));
        }
    }


    handleChange(event) {
        this.setState({selected:event.target.value});
    }

    handleSubmit() {
        if (this.state.selected == 0) {
            alert("Please select a playlist to delete.");
        }
        else if (this.refs.playlistName.value == ""){
            alert("You did not set a new name!");
        }
        else{
            fetch("http://127.0.0.1:5000/api/v1/playlists/"+this.state.selected+"/", {
                method: "PUT",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name: this.refs.playlistName.value,
                })
            })
                .then(response => {
                    if (response.status == 403) {
                        alert("This playlist is not yours!");
                        return;
                    }
                    else if (response.status == 404){
                        alert("Playlist not found.");
                        return;
                    }
                    else if (response.status == 200) {
                        alert("Playlist updated.");
                        window.location.reload();
                        return;
                    }
                    else{
                        alert("Could not update playlist.");
                        return;
                    }

                });
        }
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {

            return (
                <div id="edit_playlist">
                    <h2>Select Playlist to change name</h2>
                    <div>
                        <select onChange={this.handleChange.bind(this)}>
                            <option disabled selected value> -- select an option -- </option>
                            {this.state.playlists.map(playlist => <option value={playlist.id}
                                                                          key={playlist.id}>{playlist.name}</option>)}
                        </select>
                    </div>
                    <form id="edit_playlist_form" onSubmit={this.handleSubmit.bind(this)}>
                        <div className="form-group">
                            <h4>New Playlist Name:</h4>
                            <input type="text" className="form-control" ref="playlistName"
                                   placeholder="Enter name"/>
                        </div>
                        <button type="submit" className="btn btn-default">Submit</button>
                    </form>
                </div>
            );
        }
        else {
            return (
                <h2>Choose one of the options above!</h2>
            );
        }
    }

    render() {
        return (
            this.checkCookie()
        );
    }
}

//------------------------ ListMyPlaylists ------------------------//

class ListMyPlaylists extends React.Component {
    constructor() {
        super();
        this.state = {selected: "ascending name"};
        this.state = {playlists: []};
    }

    componentDidMount() {
        if (localStorage.getItem("token") != null) {
            fetch("http://127.0.0.1:5000/api/v1/users/self/playlists/", {
                method: "GET",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            })
                .then(result => result.json())
                .then(items => this.setState({playlists: items}));
            this.orderPlaylists.bind(this);
        }
    }

    orderPlaylists(){
        if (this.state.selected == "ascending name"){
            this.setState({playlists:window.sortAscendingByKey(this.state.playlists, "name")});
        }
        else if (this.state.selected == "descending name"){
            this.setState({playlists:window.sortDescendingByKey(this.state.playlists, "name")});
        }
        else if (this.state.selected == "ascending size"){
            this.setState({playlists:window.sortAscendingByKey(this.state.playlists, "size")});
        }
        else if (this.state.selected == "descending size"){
            this.setState({playlists:window.sortDescendingByKey(this.state.playlists, "size")});
        }
        else if (this.state.selected == "ascending date"){
            this.setState({playlists:window.sortAscendingByKey(this.state.playlists, "createdAt")});
        }
        else if (this.state.selected == "descending date"){
            this.setState({playlists:window.sortDescendingByKey(this.state.playlists, "createdAt")});
        }
        this.forceUpdate();
    }


    handleChange(event) {
        this.setState({selected:event.target.value});
        this.orderPlaylists();
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {

            return (
                <div id="edit_playlist">
                    <h2>List My Playlists by</h2>
                    <div>
                        <select onChange={this.handleChange.bind(this)}>
                            <option value="ascending name">Ascending Name</option>
                            <option value="descending name">Descending Name</option>
                            <option value="ascending size">Ascending Size</option>
                            <option value="Descending size">Descending Size</option>
                            <option value="ascending date">Ascending Creation Date</option>
                            <option value="descending date">Descending Creation Date</option>
                        </select>
                    </div>
                    <h3>Playlists</h3>
                    <ul className="playlists">
                        {this.state.playlists.map(playlist=><li key={playlist.id}>{playlist.name}</li>)}
                    </ul>
                </div>
            );
        }
        else {
            return (
                <h2>Choose one of the options above!</h2>

            );
        }
    }

    render() {
        return (
            this.checkCookie()
        );
    }
}

//------------------------ render ------------------------//

ReactDOM.render(
    <ReactRouter.Router history={ReactRouter.hashHistory}>
        <ReactRouter.Route path="/" component={App}>
            <Route path="login" component={Login}/>
            <Route path="register" component={Register}/>
            <Route path="logout" component={Logout}/>
            <Route path="updateUser" component={UpdateUser}/>
            <Route path="createPlaylist" component={CreatePlaylist}/>
            <Route path="editPlaylist" component={EditPlaylist}/>
            <Route path="listMyPlaylists" component={ListMyPlaylists}/>
            <Route path="deletePlaylist" component={DeletePlaylist}/>
        </ReactRouter.Route>
    </ReactRouter.Router>,
    container);