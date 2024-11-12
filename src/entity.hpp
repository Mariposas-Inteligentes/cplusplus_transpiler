#ifndef ENTITY
#define ENTITY

#include <string>
#include <cmath>
#include <stdexcept>

class Entity {
  private:
    std::string type;
    std::string value;

    bool check_string(Entity& other, std::string operator_type) {
        if (operator_type == "+" && other.type == "string") {
            return true;
        }
        if (operator_type == "*" && other.type == "int") {
            return true;
        }
        if (operator_type == "in" && other.type = "string") {
            return true;
        }
        if (operator_type == "not in" && other.type = "string") {
            return true;
        }
        
        return false;
    }

    bool check_number(Entity& other, std::string operator_type) {
        if (operator_type == "+" && other.type == "string") {
            return true;
        }
        if (other.typpe == "int" || other.type == "double") {
            return true;
        }
        if (operator_type == "*" && other.type == "list") {
            return true;
        }
        if (operator_type == "*" && other.type == "tuple") {
            return true;
        }
        return false;
    }

    bool check_list(Entity& other, std::string operator_type) {
        if (operator_type == "+" && other.type == "list") {
            return true;
        }
        if (operator_type == "*" && other.type == "int") {
            return true;
        }
        if (operator_type == "in") {
            return true;
        }
        if (operator_type == "not in") {
            return true;
        }
        return false;
    }

    bool check_tuple(Entity& other, std::string operator_type) {
        if (operator_type == "+" && other.type == "tuple") {
            return true;
        }
        if (operator_type == "*" && other.type == "int") {
            return true;
        }
        if (operator_type == "in") {
            return true;
        }
        if (operator_type == "not in") {
            return true;
        }
        return false;
    }

    bool check_set(Entity& other, std::string operator_type) {
        if (operator_type == "-" && other.type == "tuple") {
            return true;
        }
        if (operator_type == "in") {
            return true;
        }
        if (operator_type == "not in") {
            return true;
        }
        return false;
    }

    bool check_dict(Entity& other, std::string operator_type) {
        if (operator_type == "in") {
            return true;
        }
        if (operator_type == "not in") {
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
    operator_types:
        +, - , *, **, /, //, ^, %
        in, and, or, not in

    Types:
        int, double, string, tuple, set, dict, class
    */
   // TODO(us): implementar is operable para las diferentes comparaciones
   // o cambiar los operadores
    bool is_operable(std::string operator_type, Entity& other) {
        bool is_operable;
        switch(this->type) {  // TODO(us): Creo que el switch solo puede tener integers
            case "string":
                is_operable = check_string(other, operator_type);
                break;
            case "int": case "double":
                is_operable = check_number(other, operator_type);
                break;
            case "list":
                is_operable = check_list(other, operator_type);
                break;
            case "tuple":
                is_operable = check_tuple(other, operator_type);
                break;
            case "set":
                is_operable = check_set(other, operator_type);
                break;
            case "dict":
                is_operable = check_dict(other, operator_type);
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

   // TODO(us): dependiendo cómo guardemos una lista y así, puede que haya que cambiar
   // lo que significa sumar o restar y así (actualmente solo se concatenan cosas)

    Entity  operator+(const Entity& other) const {
        if (this->is_operable("+", other)) {
            if (this->type == "string" && other.type == "string") {
                return Entity("string", this->value + other.value);
            }
            if ((this->type == "int" || this->type == "double") && (other.type == "int" || other.type == "double")) {
                double result = std::stod(this->value) + std::stod(other.value);
                return Entity(this->type, std::to_string(result));
            }
            if (this->type == "list" && other.type == "list") {
                return Entity("list", this->value + "," + other.value); // Simple concatenation
            }
            if (this->type == "tuple" && other.type == "tuple") {
                return Entity("tuple", this->value + "," + other.value); // Simple concatenation
            }
        }
        throw std::invalid_argument("Invalid operation for the given types with +.");
    }

    Entity  operator-(const Entity& other) const {
        if (this->is_operable("-", other)) {
            if ((this->type == "int" || this->type == "double") && (other.type == "int" || other.type == "double")) {
                double result = std::stod(this->value) - std::stod(other.value);
                return Entity(this->type, std::to_string(result));
            }
            if (this->type == "set" && other.type == "set") {
                // TODO(us): hacer
                return Entity("set", ""); // Placeholder
            }
        }
        throw std::invalid_argument("Invalid operation for the given types with -.");
    }

    Entity  operator*(const Entity& other) const {
        if (this->is_operable("*", other)) {
            if (this->type == "int" && other.type == "int") {
                int result = std::stoi(this->value) * std::stoi(other.value);
                return Entity("int", std::to_string(result));
            }
            if (this->type == "string" && other.type == "int") {
                std::string result;
                int times = std::stoi(other.value);
                for (int i = 0; i < times; ++i) result += this->value;
                return Entity("string", result);
            }
            if ((this->type == "list" || this->type == "tuple") && other.type == "int") {
                std::string result;
                int times = std::stoi(other.value);
                for (int i = 0; i < times; ++i) result += this->value + ",";
                return Entity(this->type, result);
            }
        }
        throw std::invalid_argument("Invalid operation for the given types with *.");
    }

    Entity  operator/(const Entity& other) const {
        if (this->is_operable("/", other)) {
            if ((this->type == "int" || this->type == "double") && (other.type == "int" || other.type == "double")) {
                if (other.value == "0") throw std::runtime_error("Division by zero");
                double result = std::stod(this->value) / std::stod(other.value);
                return Entity(this->type, std::to_string(result));
            }
        }
        throw std::invalid_argument("Invalid operation for the given types with /.");
    }

    Entity  operator%(const Entity& other) const {
        if (this->is_operable("%", other)) {
            int result = std::stoi(this->value) % std::stoi(other.value);
            return Entity("int", std::to_string(result));
        }
        throw std::invalid_argument("Invalid operation for the given types with %.");
    }

    Entity  operator^(const Entity& other) const {
        if (this->is_operable("^", other)) {
            double result = std::pow(std::stod(this->value), std::stod(other.value));
            return Entity(this->type, std::to_string(result));
        }
        throw std::invalid_argument("Invalid operation for the given types with ^.");
    }

    // Logical and Comparison operator_types
    Entity  operator&&(const Entity& other) const {
        if (this->is_operable("and", other)) {
            bool result = (this->value != "0" && other.value != "0");
            return Entity("bool", result ? "1" : "0");
        }
        throw std::invalid_argument("Invalid operation for the given types with &&.");
    }

    Entity  operator||(const Entity& other) const {
        if (this->is_operable("or", other)) {
            bool result = (this->value != "0" || other.value != "0");
            return Entity("bool", result ? "1" : "0");
        }
        throw std::invalid_argument("Invalid operation for the given types with ||.");
    }

    // Comparison operator_types
    bool operator_type==(const Entity& other) const {
        if (this->is_operable("==", other)) {
            return this->value == other.value;
        }
        throw std::invalid_argument("Invalid operation for the given types with ==.");
    }

    bool operator_type!=(const Entity& other) const {
        if (this->is_operable("!=", other)) {
            return this->value != other.value;
        }
        throw std::invalid_argument("Invalid operation for the given types with !=.");
    }

    bool operator_type<(const Entity& other) const {
        if (this->is_operable("<", other)) {
            return std::stod(this->value) < std::stod(other.value);
        }
        throw std::invalid_argument("Invalid operation for the given types with <.");
    }

    bool operator_type>(const Entity& other) const {
        if (this->is_operable(">", other)) {
            return std::stod(this->value) > std::stod(other.value);
        }
        throw std::invalid_argument("Invalid operation for the given types with >.");
    }

    bool operator_type<=(const Entity& other) const {
        if (this->is_operable("<=", other)) {
            return std::stod(this->value) <= std::stod(other.value);
        }
        throw std::invalid_argument("Invalid operation for the given types with <=.");
    }

    bool operator_type>=(const Entity& other) const {
        if (this->is_operable(">=", other)) {
            return std::stod(this->value) >= std::stod(other.value);
        }
        throw std::invalid_argument("Invalid operation for the given types with >=.");
    }

    bool operator_type!() const {
        return this->value == "0";
    }

    // Membership operator_types

    // TODO(us): revisar que tenga sentido
    bool in(const Entity& container) const {
        if (container.is_operable("in", *this)) {
            return container.value.find(this->value) != std::string::npos;
        }
        throw std::invalid_argument("Invalid operation for 'in' with the given types.");
    }

    bool not_in(const Entity& container) const {
        return !this->in(container);
    }

};


#endif