#include <iostream>
#include <string>
#include <fstream>

using namespace std;

class User {
public:
    User(string x);
    bool reg();
    bool login();
    void del();

private:
    string usr;
    bool acc_exist();
};

User::User(string x) {
    usr = x;
}

bool User::acc_exist() {
    // sprawdzic czy istnieje plik o nazwie takiej jak username
    ifstream file(usr + ".txt");
    if (file.is_open()) {
        return true;
    }
    return false;
}

bool User::reg() {
    string pswd;
    if (usr == "") {
        cout << "Enter username: "; cin >> usr;
    }
    if (acc_exist()) {
        cout << "Account already exists ! \n"
            << "Do you want to log in? (Y/n): ";
        char x; cin >> x;
        if (x == 'Y' || x == 'y') {
            return login();
        }
    }

    cout << "Enter password: "; cin >> pswd;

    // utworzyc plik o nazwie takiej jak username i wprowadzic w niego username i password
    ofstream file(usr + ".txt");
    file << usr << '\n' << pswd;
    
    cout << "You've successfully registered." << '\n'
        << "You're now logged in." << '\n';
    return true;
}

bool User::login() {
    if (usr == "") {
        cout << "Enter username: "; cin >> usr;
    }
    if (!acc_exist()) {
        cout << "There's no account of this name ! \n"
            << "Do you want to register? (Y/n): ";
        char x; cin >> x;
        if (x == 'N' || x == 'n') {
            return false;
        }

        reg();
        cout << "You're now logged in ! \n";
        return true;
    }

    cout << "Enter password: "; 
    string pswd; cin >> pswd;
    
    // otworzyc plik o nazwie takiej jak username i sprawdzic czy haslo sie zgadza
    ifstream read(usr + ".txt");
    string comp_usr, comp_pswd;
    read >> comp_usr >> comp_pswd;

    if (comp_usr == usr && comp_pswd == pswd) {
        cout << "Successfully logged in ! \n";
        return true;
    }
    cout << "Incorrect password ! \n";
    return false;
}

void User::del() {
    if (!acc_exist()) {
        cout << "There's no such user ! \n";
        return;
    }

    cout << "Enter password: \n";
    string pswd; cin >> pswd;
    ifstream read(usr + ".txt");
    string comp_usr, comp_pswd;
    read >> comp_usr >> comp_pswd;
    read.close();
    if (pswd != comp_pswd) {
        cout << "Incorrect password ! \n"
            << "Account not deleted \n";
        return;
    }
        
    usr.append(".txt");
    const char* file = usr.data();
    int res = remove(file);

    if (!res) {
        cout << "Account successfully deleted ! \n";
    }
    else {
        cout << "Error ! \n"
            << "Account not deleted \n";
    }
}

int main(void)
{
    cout << "Choose an operation: \n";
    cout << "r: Register \n";
    cout << "l: Login \n";
    cout << "d: Delete account \n";
    char ch; cin >> ch;

    cout << "Enter username: ";
    string s; cin >> s;
    User user(s);

    bool logged_in = false;
    switch (ch) {
    case 'r':
        logged_in = user.reg();
        break;
    case 'l':
        logged_in = user.login();
        break;
    case 'd':
        user.del();
        break;
    default:
        cout << "Invalid input ! \n";
        break;
    }
}