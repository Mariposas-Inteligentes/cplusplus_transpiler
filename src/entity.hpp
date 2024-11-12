#ifndef ENTITY
#define ENTITY

#include <string>

class Entity {
  private:
    std::string type;
    std::string value;

    bool check_string(Entity& other, std::string operator) {
        if (operator == "+" && other.type == "string") {
            return true;
        }
        if (operator == "*" && other.type == "int") {
            return true;
        }
        if (operator == "in" && other.type = "string") {
            return true;
        }
        if (operator == "not in" && other.type = "string") {
            return true;
        }
        
        return false;
    }

    bool check_number(Entity& other, std::string operator) {
        if (operator == "+" && other.type == "string") {
            return true;
        }
        if (other.typpe == "int" || other.type == "double") {
            return true;
        }
        if (operator == "*" && other.type == "list") {
            return true;
        }
        if (operator == "*" && other.type == "tuple") {
            return true;
        }
        return false;
    }

    bool check_list(Entity& other, std::string operator) {
        if (operator == "+" && other.type == "list") {
            return true;
        }
        if (operator == "*" && other.type == "int") {
            return true;
        }
        if (operator == "in") {
            return true;
        }
        if (operator == "not in") {
            return true;
        }
        return false;
    }

    bool check_tuple(Entity& other, std::string operator) {
        if (operator == "+" && other.type == "tuple") {
            return true;
        }
        if (operator == "*" && other.type == "int") {
            return true;
        }
        if (operator == "in") {
            return true;
        }
        if (operator == "not in") {
            return true;
        }
        return false;
    }

    bool check_set(Entity& other, std::string operator) {
        if (operator == "-" && other.type == "tuple") {
            return true;
        }
        if (operator == "in") {
            return true;
        }
        if (operator == "not in") {
            return true;
        }
        return false;
    }

    bool check_dict(Entity& other, std::string operator) {
        if (operator == "in") {
            return true;
        }
        if (operator == "not in") {
            return true;
        }
        return false;
    }

  public:
    Entity(std::string type, std::string value) {
        this->type = type;
        this->value = value;
    }

    /*
    Operators:
        +, - , *, **, /, //, ^, %
        in, and, or, not in

    Types:
        int, double, string, tuple, set, dict, class
    */
    bool is_operable(std::string operator, Entity other) {
        bool is_operable;
        switch(this.type) {
            case "string":
                is_operable = check_string(other, operator);
                break;
            case "int": case "double":
                is_operable = check_number(other, operator);
                break;
            case "list":
                is_operable = check_list(other, operator);
                break;
            case "tuple":
                is_operable = check_tuple(other, operator);
                break;
            case "set":
                is_operable = check_set(other, operator);
                break;
            case "dict":
                is_operable = check_dict(other, operator);
                break;
            case "class":
                is_operable = true;
                break;
        }
        return is_operable;
    }

    void set_type(std::string type){
        this->type = type;
    }
    
    void set_value(std::string value){
        this->value = value;
    }
    
    std::string get_type(){
        return type;
    }
    
    std::string get_value(){
        return value;
    }

    // TODO(us): sobrecargar operadores: +, =
};


#endif