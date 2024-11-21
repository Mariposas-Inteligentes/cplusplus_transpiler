#include "entity.hpp"



#include <cmath>
#include <iostream>
#include <string>
#include <stdexcept>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <algorithm>

#ifndef ENTITY_ITERATOR
#define ENTITY_ITERATOR

class Entity;

class Iterator{
  public:
    friend class Entity;
  
  private:
    Entity* object;
    int type;
    std::vector<Entity>::iterator list_iter;
    std::vector<Entity>::iterator list_end;
    std::vector<Entity>::iterator tuple_iter;
    std::vector<Entity>::iterator tuple_end;
    std::unordered_set<Entity, Entity::HashFunction, Entity::EqualsComparator>::iterator set_iter;
    std::unordered_set<Entity, Entity::HashFunction, Entity::EqualsComparator>::iterator set_end;
    std::unordered_map<Entity, Entity, Entity::HashFunction, Entity::EqualsComparator>::iterator dict_iter;
    std::unordered_map<Entity, Entity, Entity::HashFunction, Entity::EqualsComparator>::iterator dict_end;

  public:
    Iterator() {
        this->type = INT;
        this->object = NULL;
    }
    Iterator(Entity* object) {
        this->type = object->get_type();
        this->object = object;
        this->initialize_iterator();
    }

    void initialize_iterator() {
        switch (this->type) {
            case LIST:
                this->list_iter = this->object->list.begin();
                this->list_end = this->object->list.end();
                break;
            case TUPLE:
                this->tuple_iter = this->object->tuple.begin();
                this->tuple_end = this->object->tuple.end();
                break;
            case SET:
                this->set_iter = this->object->set.begin();
                this->set_end = this->object->set.end();
                break;
            case DICT:
                this->dict_iter = this->object->dict.begin();
                this->dict_end = this->object->dict.end();
                break;
            default:
                throw std::runtime_error("Unsupported type for iterator");
        }
    }

    Entity next() {
      switch(this->type) {
        case LIST:
            return *this->list_iter++;
        case TUPLE:
            return *this->tuple_iter++;
        case SET:
            return *this->set_iter++;
        case DICT:
            return this->dict_iter++->first;
        default:
            throw std::runtime_error("Unsupported type for iterator");  
        }
    }

    bool has_next() const {
        switch (this->type) {
            case LIST:
                return this->list_iter != this->list_end;
            case TUPLE:
                return this->tuple_iter != this->tuple_end;
            case SET:
                return this->set_iter != this->set_end;
            case DICT:
                return this->dict_iter != this->dict_end;
            default:
                throw std::runtime_error("Unsupported type for iterator");
        }
    }
};

#endif
