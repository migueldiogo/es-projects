var {
    Router,
    Route,
    IndexRoute,
    IndexLink,
    hashHistory,
    Link
} = ReactRouter;

var SERVER_URL = "http://soundshare-env.tspig2m4ea.eu-west-1.elasticbeanstalk.com"

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
                                <li><Link to="/songsFromPlaylist" activeClassName="active">List Songs</Link>
                                </li>
                                <li><Link to="/deletePlaylist" activeClassName="active">Delete Playlist</Link></li>
                            </ul>
                        </li>
                        <li className="dropdown"><a>Songs</a>
                            <ul>
                                <li><Link to="/uploadSong" activeClassName="active">Upload Song</Link></li>
                                <li><Link to="/editSong" activeClassName="active">Edit Song</Link></li>
                                <li><Link to="/listSongs" activeClassName="active">List All Songs</Link></li>
                                <li><Link to="/findSongs" activeClassName="active">Search Songs</Link></li>
                                <li><Link to="/deleteSong" activeClassName="active">Delete Song</Link></li>
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
            fetch(SERVER_URL + "/api/v1/users/self/tokens/", {
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
            fetch(SERVER_URL + "/api/v1/users/", {
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
        fetch(SERVER_URL + "/api/v1/users/self/", {
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
        fetch(SERVER_URL + "/api/v1/users/self/" + this.state.id + "/", {
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
            fetch(SERVER_URL + "/api/v1/playlists/", {
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
            fetch(SERVER_URL + "/api/v1/users/self/playlists/", {
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
        this.setState({selected: event.target.value});
    }

    handleClick() {
        if (this.state.selected == 0) {
            alert("Please select a playlist to delete.");
        }
        else {
            fetch(SERVER_URL + "/api/v1/playlists/" + this.state.selected + "/", {
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
                    else if (response.status == 404) {
                        alert("Playlist not found.");
                        return;
                    }
                    else if (response.status == 200) {
                        alert("Playlist deleted.");
                        window.location.reload();
                        return;
                    }
                    else {
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
                            <option disabled selected value> -- select an option --</option>
                            {this.state.playlists.map(playlist => <option value={playlist.id}
                                                                          key={playlist.id}>{playlist.name}</option>)}
                        </select>
                    </div>
                    <button id="delete_playlist" className="btn btn-default" onClick={this.handleClick.bind(this)}>
                        Delete
                    </button>
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
            fetch(SERVER_URL + "/api/v1/users/self/playlists/", {
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
        this.setState({selected: event.target.value});
    }

    handleSubmit() {
        if (this.state.selected == 0) {
            alert("Please select a playlist to delete.");
        }
        else if (this.refs.playlistName.value == "") {
            alert("You did not set a new name!");
        }
        else {
            fetch(SERVER_URL + "/api/v1/playlists/" + this.state.selected + "/", {
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
                    else if (response.status == 404) {
                        alert("Playlist not found.");
                        return;
                    }
                    else if (response.status == 200) {
                        alert("Playlist updated.");
                        window.location.reload();
                        return;
                    }
                    else {
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
                            <option disabled selected value> -- select an option --</option>
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
            fetch(SERVER_URL + "/api/v1/users/self/playlists/", {
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
        if (event.target.value == "ascending name") {
            this.setState({playlists: window.sortAscendingByKey(this.state.playlists, "name")});
        }
        else if (event.target.value == "descending name") {
            this.setState({playlists: window.sortDescendingByKey(this.state.playlists, "name")});
        }
        else if (event.target.value == "ascending size") {
            this.setState({playlists: window.sortAscendingByKey(this.state.playlists, "size")});
        }
        else if (event.target.value == "descending size") {
            this.setState({playlists: window.sortDescendingByKey(this.state.playlists, "size")});
        }
        else if (event.target.value == "ascending date") {
            this.setState({playlists: window.sortAscendingByKey(this.state.playlists, "createdAt")});
        }
        else if (event.target.value == "descending date") {
            this.setState({playlists: window.sortDescendingByKey(this.state.playlists, "createdAt")});
        }
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {

            return (
                <div id="edit_playlist">
                    <h2>List My Playlists by</h2>
                    <div>
                        <select onChange={this.handleChange.bind(this)}>
                            <option disabled selected value> -- select an option --</option>
                            <option value="ascending name">Ascending Name</option>
                            <option value="descending name">Descending Name</option>
                            <option value="ascending size">Ascending Size</option>
                            <option value="descending size">Descending Size</option>
                            <option value="ascending date">Ascending Creation Date</option>
                            <option value="descending date">Descending Creation Date</option>
                        </select>
                    </div>
                    <h3>Playlists</h3>
                    <ul className="playlists">
                        {this.state.playlists.map(playlist => <li key={playlist.id}><p><b>Name: </b>{playlist.name}</p>
                            <p><b>Size: </b>{playlist.size} musics</p><p><b>Creation Date: </b>{playlist.createdAt}</p>
                        </li>)}
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

//------------------------ UploadSong ------------------------//

class UploadSong extends React.Component {
    constructor() {
        super();
        this.state = {form: ""};
    }

    handleSubmit() {
        if (this.refs.songTitle.value == "" || this.refs.songArtist.value == "" || this.refs.songAlbum.value == "" || this.refs.songYear.value == "" || this.refs.songFile.value == "") {
            alert("Please fill all the fields.");
        }
        else {
            let formdata = new FormData();
            formdata.append("title", this.refs.songTitle.value);
            formdata.append("artist", this.refs.songArtist.value);
            formdata.append("album", this.refs.songAlbum.value);
            formdata.append("releaseYear", this.refs.songYear.value);
            formdata.append("file", this.refs.songFile.files[0]);
            fetch(SERVER_URL + "/api/v1/songs/", {
                method: "POST",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                },
                body: formdata,
            })
                .then(response => response.status)
                .then(code => {
                    if (code == 200) {
                        alert("Song successfully uploaded!");
                        window.location.reload();
                    }
                    else if (code == 400) {
                        alert("Invalid file extension!");
                    }
                    else {
                        alert("Could not upload song.");
                    }
                });
        }
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {
            return (
                <div id="create_playlist">
                    <h2>Upload Song</h2>
                    <form id="upload_song_form" onSubmit={this.handleSubmit.bind(this)}>
                        <div className="form-group">
                            <h4>Title:</h4>
                            <input type="text" className="form-control" ref="songTitle"
                                   placeholder="Enter title"/>
                        </div>
                        <div className="form-group">
                            <h4>Artist:</h4>
                            <input type="text" className="form-control" ref="songArtist"
                                   placeholder="Enter artist"/>
                        </div>
                        <div className="form-group">
                            <h4>Album:</h4>
                            <input type="text" className="form-control" ref="songAlbum"
                                   placeholder="Enter album"/>
                        </div>
                        <div className="form-group">
                            <h4>Release Year:</h4>
                            <input type="number" className="form-control" ref="songYear"
                                   placeholder="Enter year"/>
                        </div>
                        <div className="form-group">
                            <h4>File of the song:</h4>
                            <input type="file" ref="songFile" accept=".mp3,.wav"/>
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

//------------------------ DeleteSong ------------------------//

class DeleteSong extends React.Component {
    constructor() {
        super();
        this.state = {selected: 0};
        this.state = {songs: []};
    }

    componentDidMount() {
        if (localStorage.getItem("token") != null) {
            fetch(SERVER_URL + "/api/v1/users/self/songs/", {
                method: "GET",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            })
                .then(result => result.json())
                .then(items => this.setState({songs: items}));
        }
    }


    handleChange(event) {
        this.setState({selected: event.target.value});
    }

    handleClick() {
        if (this.state.selected == 0) {
            alert("Please select a song to delete.");
        }
        else {
            fetch(SERVER_URL + "/api/v1/songs/" + this.state.selected + "/", {
                method: "DELETE",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            })
                .then(response => {
                    if (response.status == 403) {
                        alert("This song is not yours!");
                        return;
                    }
                    else if (response.status == 404) {
                        alert("Song not found.");
                        return;
                    }
                    else if (response.status == 200) {
                        alert("Song deleted.");
                        window.location.reload();
                        return;
                    }
                    else {
                        alert("Could not delete song.");
                        return;
                    }

                });
        }
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {

            return (
                <div id="delete_song">
                    <h2>Select Song To Delete</h2>
                    <div>
                        <select onChange={this.handleChange.bind(this)}>
                            <option disabled selected value> -- select an option --</option>
                            {this.state.songs.map(song => <option value={song.id}
                                                                  key={song.id}>{song.title}</option>)}
                        </select>
                    </div>
                    <button id="delete_song" className="btn btn-default" onClick={this.handleClick.bind(this)}>Delete
                    </button>
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

//------------------------ EditSong ------------------------//

class EditSong extends React.Component {
    constructor() {
        super();
        this.state = {selected: 0};
        this.state = {songs: []};
    }

    componentDidMount() {
        if (localStorage.getItem("token") != null) {
            fetch(SERVER_URL + "/api/v1/users/self/songs/", {
                method: "GET",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            })
                .then(result => result.json())
                .then(items => this.setState({songs: items}));
        }
    }


    handleChange(event) {
        this.setState({selected: event.target.value});
    }

    handleSubmit() {
        if (this.state.selected == 0) {
            alert("Please select a song to delete.");
        }
        else {
            let formdata = new FormData();
            if (this.refs.songTitle.value != "") {
                formdata.append("title", this.refs.songTitle.value);
            }
            if (this.refs.songArtist.value != "") {
                formdata.append("artist", this.refs.songArtist.value);
            }
            if (this.refs.songAlbum.value != "") {
                formdata.append("album", this.refs.songAlbum.value);
            }
            if (this.refs.songYear.value != "") {
                formdata.append("releaseYear", this.refs.songYear.value);
            }
            if (this.refs.songFile.value != "") {
                formdata.append("file", this.refs.songFile.files[0]);
            }
            fetch(SERVER_URL + "/api/v1/songs/" + this.state.selected + "/", {
                method: "PUT",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                },
                body: formdata,
            })
                .then(response => {
                    if (response.status == 403) {
                        alert("This song is not yours!");
                        return;
                    }
                    else if (response.status == 404) {
                        alert("Song not found.");
                        return;
                    }
                    else if (response.status == 200) {
                        alert("Song updated.");
                        window.location.reload();
                        return;
                    }
                    else {
                        alert("Could not update song.");
                        return;
                    }

                });
        }
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {

            return (
                <div id="edit_song">
                    <h2>Select Song to edit</h2>
                    <div>
                        <select onChange={this.handleChange.bind(this)}>
                            <option disabled selected value> -- select an option --</option>
                            {this.state.songs.map(song => <option value={song.id}
                                                                  key={song.id}>{song.title}</option>)}
                        </select>
                    </div>
                    <form id="edit_song_form" onSubmit={this.handleSubmit.bind(this)}>
                        <div className="form-group">
                            <h4>New Title:</h4>
                            <input type="text" className="form-control" ref="songTitle"
                                   placeholder="Enter title"/>
                        </div>
                        <div className="form-group">
                            <h4>New Artist:</h4>
                            <input type="text" className="form-control" ref="songArtist"
                                   placeholder="Enter artist"/>
                        </div>
                        <div className="form-group">
                            <h4>New Album:</h4>
                            <input type="text" className="form-control" ref="songAlbum"
                                   placeholder="Enter album"/>
                        </div>
                        <div className="form-group">
                            <h4>New Release Year:</h4>
                            <input type="number" className="form-control" ref="songYear"
                                   placeholder="Enter year"/>
                        </div>
                        <div className="form-group">
                            <h4>New File of the song:</h4>
                            <input type="file" ref="songFile" accept=".mp3,.wav"/>
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

//------------------------ ListSongs ------------------------//

class ListSongs extends React.Component {
    constructor() {
        super();
        this.state = {pSelected: 0};
        this.state = {songs: [], playlists: []};
    }

    componentDidMount() {
        if (localStorage.getItem("token") != null) {
            fetch(SERVER_URL + "/api/v1/songs", {
                method: "GET",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            })
                .then(result => result.json())
                .then(items => this.setState({songs: items}));
            fetch(SERVER_URL + "/api/v1/users/self/playlists/", {
                method: "GET",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            })
                .then(resultP => resultP.json())
                .then(itemsP => this.setState({playlists: itemsP}));
        }
    }

    handleChange(event){
        this.setState({pSelected:event.target.value});
    }

    addSong(event) {
        fetch(SERVER_URL + "/api/v1/playlists/" + this.state.pSelected + "/songs/" + event.target.value + "/", {
            method: "POST",
            headers: {
                "Authorization": localStorage.getItem("token"),
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body: "",
        })
            .then(response => response.status)
            .then(code => {
                if (code == 200) {
                    alert("Song successfully added to playlist!");
                    window.location.reload();
                }
                else if (code == 403) {
                    alert("You cannot add this song to this playlist!");
                }
                else if (code == 404) {
                    alert("Playlist/Song not found!");
                }
                else {
                    alert("Could not upload song.");
                }
            });
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {

            return (
                <div id="edit_playlist">
                    <h2>List Of All Songs In Soundshare</h2>
                    <ul className="songs">
                        {this.state.songs.map(song => <li key={song.id}><p><b>Title: </b>{song.title}</p>
                            <p><b>Artist: </b>{song.artist}</p><p><b>Album: </b>{song.album}</p><p><b>Release
                                Year: </b>{song.releaseYear}</p>
                            <div>
                                <audio controls>
                                    <source src={song.url} type="audio/mpeg"/>
                                </audio>
                            </div>
                            <p>Add to playlist: </p>
                            <select onChange={this.handleChange.bind(this)}>
                                <option disabled selected value> -- select an option --</option>
                                {this.state.playlists.map(playlist => <option value={playlist.id}
                                                                      key={playlist.id}>{playlist.name}</option>)}
                            </select>
                            <button type="submit" className="btn btn-default btn-sm" value={song.id}
                                    onClick={this.addSong.bind(this)}>
                                Add Song
                            </button>
                        </li>)}
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

//------------------------ FindSongs ------------------------//

class FindSongs extends React.Component {
    constructor() {
        super();
        this.state = {pSelected: 0};
        this.state = {songs: [], playlists: []};
    }

    componentDidMount() {
        if (localStorage.getItem("token") != null) {
            fetch(SERVER_URL + "/api/v1/users/self/playlists/", {
                method: "GET",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            })
                .then(resultP => resultP.json())
                .then(itemsP => this.setState({playlists: itemsP}));
        }
    }

    handleSubmit() {
        let args = "";
        if (this.refs.songTitle.value == "" && this.refs.songArtist.value == "") {
            alert("Please fill one of the fields.");
        }
        else if (this.refs.songTitle.value != "" && this.refs.songArtist.value != "") {
            args = "?title=" + this.refs.songTitle.value + "&artist=" + this.refs.songArtist.value;
        }
        else if (this.refs.songTitle.value != "" && this.refs.songArtist.value == "") {
            args = "?title=" + this.refs.songTitle.value;
        }
        else if (this.refs.songTitle.value == "" && this.refs.songArtist.value != "") {
            args = "?artist=" + this.refs.songArtist.value;
        }
        fetch(SERVER_URL + "/api/v1/songs" + args, {
            method: "GET",
            headers: {
                "Authorization": localStorage.getItem("token"),
                "Accept": "application/json",

            }
        })
            .then(result => result.json())
            .then(items => this.setState({songs: items}));
    }

    handleChange(event){
        this.setState({pSelected:event.target.value});
    }

    addSong(event) {
        fetch(SERVER_URL + "/api/v1/playlists/" + this.state.pSelected + "/songs/" + event.target.value + "/", {
            method: "POST",
            headers: {
                "Authorization": localStorage.getItem("token"),
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body: "",
        })
            .then(response => response.status)
            .then(code => {
                if (code == 200) {
                    alert("Song successfully added to playlist!");
                    window.location.reload();
                }
                else if (code == 403) {
                    alert("You cannot add this song to this playlist!");
                }
                else if (code == 404) {
                    alert("Playlist/Song not found!");
                }
                else {
                    alert("Could not upload song.");
                }
            });
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {
            return (
                <div id="create_playlist">
                    <h2>Search Songs By:</h2>
                    <form id="search_song_form" onSubmit={this.handleSubmit.bind(this)}>
                        <div className="form-group">
                            <h4>Title:</h4>
                            <input type="text" className="form-control" ref="songTitle"
                                   placeholder="Enter title"/>
                        </div>
                        <div className="form-group">
                            <h4>Artist:</h4>
                            <input type="text" className="form-control" ref="songArtist"
                                   placeholder="Enter artist"/>
                        </div>
                        <button type="submit" className="btn btn-default">Search</button>
                    </form>
                    <h2>Results</h2>
                    <ul className="songs">
                        {this.state.songs.map(song => <li key={song.id}><p><b>Title: </b>{song.title}</p>
                            <p><b>Artist: </b>{song.artist}</p><p><b>Album: </b>{song.album}</p><p><b>Release
                                Year: </b>{song.releaseYear}</p>
                            <div>
                                <audio controls>
                                    <source src={song.url} type="audio/mpeg"/>
                                </audio>
                            </div>
                            <p>Add to playlist: </p>
                            <select onChange={this.handleChange.bind(this)}>
                                <option disabled selected value> -- select an option --</option>
                                {this.state.playlists.map(playlist => <option value={playlist.id}
                                                                      key={playlist.id}>{playlist.name}</option>)}
                            </select>
                            <button type="submit" className="btn btn-default btn-sm" value={song.id}
                                    onClick={this.addSong.bind(this)}>
                                Add Song
                            </button>
                        </li>)}
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

//------------------------ SongsFromPlaylist ------------------------//

class SongsFromPlaylist extends React.Component {
    constructor() {
        super();
        this.state = {pSelected: 0, sSelected: 0};
        this.state = {thisSongs: [], songs: [], playlists: []};
    }

    componentDidMount() {
        if (localStorage.getItem("token") != null) {
            fetch(SERVER_URL + "/api/v1/users/self/playlists/", {
                method: "GET",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            })
                .then(resultP => resultP.json())
                .then(itemsP => this.setState({playlists: itemsP}));
            fetch(SERVER_URL + "/api/v1/users/self/songs/", {
                method: "GET",
                headers: {
                    "Authorization": localStorage.getItem("token"),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            })
                .then(resultP => resultP.json())
                .then(itemsP => this.setState({songs: itemsP}));
        }
    }


    handleChange(event) {
        this.setState({pSelected: event.target.value});
        fetch(SERVER_URL + "/api/v1/playlists/" + event.target.value + "/songs/", {
            method: "GET",
            headers: {
                "Authorization": localStorage.getItem("token"),
                "Accept": "application/json",
            }
        })
            .then(resultS => resultS.json())
            .then(itemsS => this.setState({thisSongs: itemsS}));
    }

    selectSong(event) {
        this.setState({sSelected: event.target.value});
    }

    addSong(event) {
        fetch(SERVER_URL + "/api/v1/playlists/" + this.state.pSelected + "/songs/" + this.state.sSelected + "/", {
            method: "POST",
            headers: {
                "Authorization": localStorage.getItem("token"),
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body: "",
        })
            .then(response => response.status)
            .then(code => {
                if (code == 200) {
                    alert("Song successfully added to playlist!");
                    window.location.reload();
                }
                else if (code == 403) {
                    alert("You cannot add this song to this playlist!");
                }
                else if (code == 404) {
                    alert("Playlist/Song not found!");
                }
                else {
                    alert("Could not upload song.");
                }
            });
    }

    deleteSong(event) {
        console.log(event.target.value);
        fetch(SERVER_URL + "/api/v1/playlists/" + this.state.pSelected + "/songs/" + event.target.value + "/", {
            method: "DELETE",
            headers: {
                "Authorization": localStorage.getItem("token"),
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        })
            .then(response => {
                if (response.status == 403) {
                    alert("This playlist/song is not yours!");
                    return;
                }
                else if (response.status == 404) {
                    alert("Playlist/song not found.");
                    return;
                }
                else if (response.status == 200) {
                    alert("Song deleted from playlist.");
                    window.location.reload();
                    return;
                }
                else {
                    alert("Could not delete song from playlist.");
                    return;
                }

            });
    }

    checkCookie() {
        if (localStorage.getItem("token") != null) {
            return (
                <div id="playlist_songs">
                    <h2>List Songs From Playlist:</h2>
                    <div>
                        <select onChange={this.handleChange.bind(this)}>
                            <option disabled selected value> -- select an option --</option>
                            {this.state.playlists.map(playlist => <option value={playlist.id}
                                                                          key={playlist.id}>{playlist.name}</option>)}
                        </select>
                    </div>
                    <h3>Add Song:</h3>
                    <div>
                        <select onChange={this.selectSong.bind(this)}>
                            <option disabled selected value> -- select an option --</option>
                            {this.state.songs.map(song => <option value={song.id}
                                                                  key={song.id}>{song.title}</option>)}
                        </select>
                    </div>
                    <div>
                        <button id="add_song_btn" type="submit" className="btn btn-default"
                                onClick={this.addSong.bind(this)}>Add
                        </button>
                    </div>
                    <h3>Songs:</h3>
                    <ul className="songs">
                        {this.state.thisSongs.map(song => <li key={song.id}><p><b>Title: </b>{song.title}</p>
                            <p><b>Artist: </b>{song.artist}</p><p><b>Album: </b>{song.album}</p><p><b>Release
                                Year: </b>{song.releaseYear}</p>
                            <div>
                                <audio controls>
                                    <source src={song.url} type="audio/mpeg"/>
                                </audio>
                            </div>
                            <button type="submit" className="btn btn-default btn-sm" value={song.id}
                                    onClick={this.deleteSong.bind(this)}>
                                Delete Song
                            </button>
                        </li>)}
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
            <Route path="uploadSong" component={UploadSong}/>
            <Route path="deleteSong" component={DeleteSong}/>
            <Route path="editSong" component={EditSong}/>
            <Route path="listSongs" component={ListSongs}/>
            <Route path="findSongs" component={FindSongs}/>
            <Route path="songsFromPlaylist" component={SongsFromPlaylist}/>
        </ReactRouter.Route>
    </ReactRouter.Router>,
    container);