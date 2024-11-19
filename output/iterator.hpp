#include "entity.hpp"

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
    std::vector<Entity>::iterator tuple_iter;
    std::unordered_set<Entity, Entity::HashFunction, Entity::EqualsComparator>::iterator set_iter;
    std::unordered_map<Entity, Entity, Entity::HashFunction, Entity::EqualsComparator>::iterator dict_iter;

  public:
    Iterator(Entity* object) {
        this->type = object->type;
        this->object = object;
        this->initialize_iterator();
    }

    void initialize_iterator() {
        switch(this->type) {
            case LIST:
                this->list_iter = this->object->list.begin();
                break;
            case TUPLE:
                this->tuple_iter = this->object->tuple.begin();
                break;
            case SET:
                this->set_iter = this->object->set.begin();
                break;
            case DICT:
                this->dict_iter = this->object->dict.begin();
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
            return *this->dict_iter++;
        default:
            throw std::runtime_error("Unsupported type for iterator");  
        }
    }
};

#endif
