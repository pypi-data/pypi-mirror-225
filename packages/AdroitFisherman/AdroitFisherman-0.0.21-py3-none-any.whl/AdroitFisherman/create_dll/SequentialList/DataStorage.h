#ifndef DATAHANDLER_H_INCLUDED
#define DATAHANDLER_H_INCLUDED
#include <iostream>
using namespace std;
namespace DataStorage
{
    template <class T>
    class SequentialList
    {
    public:
        SequentialList(int maxsize = 255) :max_size(maxsize) {}
        void SetCapacity(int max_size);
        bool InitList();
        void DestroyList();
        void ClearList();
        bool ListEmpty();
        int ListLength();
        T GetElem(int index);
        int LocateElem(T elem);
        T PriorElem(T elem);
        T NextElem(T elem);
        bool ListInsert(int index, T elem);
        bool ListDelete(int index);
        void TraverseList();
    private:
        T* elem;
        int length;
        int max_size;
    };
    template <class T>
    void SequentialList<T>::SetCapacity(int maxsize)
    {
        this->max_size = maxsize;
    }
    template <class T>
    bool SequentialList<T>::InitList()
    {
        this->elem = new T[max_size];
        if (this->elem != NULL)
        {
            length = 0;
            return true;
        }
        else if (this->elem == NULL)
        {
            return false;
        }
    }
    template <class T>
    void SequentialList<T>::DestroyList()
    {
        delete[]this->elem;
        this->elem = NULL;
        this->length = NULL;
    }
    template <class T>
    void SequentialList<T>::ClearList()
    {
        size_t i{ 0 };
        while (i < this->max_size)
        {
            this->elem[i] = NULL;
            i++;
        }
        this->length = 0;
    }
    template <class T>
    bool SequentialList<T>::ListEmpty()
    {
        if (this->length != 0)
        {
            return false;
        }
        else
        {
            return true;
        }
    }
    template <class T>
    int SequentialList<T>::ListLength()
    {
        return this->length;
    }
    template <class T>
    T SequentialList<T>::GetElem(int index)
    {
        if (index<0 || index>=this->length)
        {
            return NULL;
        }
        else
        {
            return this->elem[index];
        }
    }
    template <class T>
    int SequentialList<T>::LocateElem(T elem)
    {
        int i = 0;
        while (i < this->length)
        {
            if (this->elem[i] == elem)
            {
                return i;
            }
            i++;
        }
        return -1;
    }
    template <class T>
    T SequentialList<T>::PriorElem(T elem)
    {
        int counter = 0;
        T result = NULL;
        while (counter < this->length)
        {
            if (this->elem[counter] == elem && counter != 0)
            {
                result = this->elem[counter - 1];
                break;
            }
            counter++;
        }
        return result;
    }
    template <class T>
    T SequentialList<T>::NextElem(T elem)
    {
        int counter = 0;
        T result = NULL;
        while (counter < this->length)
        {
            if (this->elem[counter] == elem && counter + 1 != length)
            {
                result = this->elem[counter + 1];
                break;
            }
            counter++;
        }
        return result;
    }
    template <class T>
    bool SequentialList<T>::ListInsert(int index, T elem)
    {
        if (index<0 || index>this->length)
        {
            return false;
        }
        else
        {
            if (length >= max_size)
            {
                return false;
            }
            else
            {
                for (int i = this->length; i >= index; i--)
                {
                    this->elem[i] = this->elem[i - 1];
                }
                this->elem[index] = elem;
                ++this->length;
                return true;
            }
        }
    }
    template <class T>
    bool SequentialList<T>::ListDelete(int index)
    {
        if (index<0 || index>this->length - 1)
        {
            return false;
        }
        else
        {
            for (int i = index; i < this->length; i++)
            {
                this->elem[i] = this->elem[i + 1];
            }
            this->elem[this->length - 1] = NULL;
            --this->length;
            return true;
        }
    }
    template <class T>
    void SequentialList<T>::TraverseList()
    {
        for (int i = 0; i < this->length; i++)
        {
            cout << this->elem[i] << "\t";
        }
        cout << endl;
    }
    template <class T>
    class SingleLinkedList
    {
    public:
        SingleLinkedList() :List(NULL), length(0) {}
        bool InitList();
        void DestroyList();
        void ClearList();
        bool ListEmpty();
        int ListLength();
        T GetElem(int index);
        int LocateElem(T elem);
        T PriorElem(T elem);
        T NextElem(T elem);
        bool addFirst(T elem);
        bool addAfter(T elem);
        bool ListInsert(int index, T elem);
        bool ListDelete(int index);
        void TraverseList();
    private:
        typedef struct Node {
            T elem;
            struct Node* next;
        }*LinkedList, LNode;
        LinkedList List;
        int length;
    };
    template <class T>
    bool SingleLinkedList<T>::InitList()
    {
        this->List = new LNode();
        if (this->List != NULL)
        {
            this->List->elem = NULL;
            this->List->next = NULL;
            return true;
        }
        else
        {
            return false;
        }
    }
    template <class T>
    void SingleLinkedList<T>::DestroyList()
    {
        LNode* p = this->List;
        while (this->List->next != NULL)
        {
            p = this->List->next;
            this->List->next = p->next;
            delete p;
            p = NULL;
        }
        this->List = NULL;
        this->length = 0;
    }
    template <class T>
    void SingleLinkedList<T>::ClearList()
    {
        LNode* p = this->List;
        while (this->List->next != NULL)
        {
            p = this->List->next;
            this->List->next = p->next;
            delete p;
            p = NULL;
        }
        this->length = 0;
    }
    template <class T>
    bool SingleLinkedList<T>::ListEmpty()
    {
        if (this->List->next != NULL)
        {
            return false;
        }
        else
        {
            return true;
        }
    }
    template <class T>
    int SingleLinkedList<T>::ListLength()
    {
        return this->length;
    }
    template <class T>
    T SingleLinkedList<T>::GetElem(int index)
    {
        if (index < 0 || index >= this->length)
        {
            return NULL;
        }
        else
        {
            LNode* p = this->List->next;
            int counter = 0;
            while (counter < index)
            {
                p = p->next;
                counter++;
            }
            return p->elem;
        }
    }
    template <class T>
    int SingleLinkedList<T>::LocateElem(T elem)
    {
        LNode* p = this->List->next;
        int i = 0;
        while (i < this->length && p != NULL)
        {
            if (p->elem == elem)
            {
                return i;
            }
            p = p->next;
            i++;
        }
        return -1;
    }
    template <class T>
    T SingleLinkedList<T>::PriorElem(T elem)
    {
        LNode* p = this->List->next;
        while (p->next != NULL)
        {
            if (p->next->elem == elem)
            {
                return p->elem;
            }
            p = p->next;
        }
        return NULL;
    }
    template <class T>
    T SingleLinkedList<T>::NextElem(T elem)
    {
        LNode* p = this->List->next;
        while (p->next != NULL)
        {
            if (p->elem == elem)
            {
                return p->next->elem;
            }
            p = p->next;
        }
        return NULL;
    }
    template <class T>
    bool SingleLinkedList<T>::addFirst(T elem)
    {
        LNode* s;
        s = new LNode();
        if (s != NULL)
        {
            s->elem = elem;
            s->next = this->List->next;
            this->List->next = s;
            this->length++;
            return true;
        }
        else
        {
            return false;
        }
    }
    template <class T>
    bool SingleLinkedList<T>::addAfter(T elem)
    {
        LNode* s, * p = this->List;
        s = new LNode();
        if (s != NULL)
        {
            s->elem = elem;
            while (p->next != NULL)
            {
                p = p->next;
            }
            s->next = p->next;
            p->next = s;
            this->length++;
            return true;
        }
        else
        {
            return false;
        }
    }
    template <class T>
    bool SingleLinkedList<T>::ListInsert(int index, T elem)
    {
        if (index<0 || index>this->length)
        {
            return false;
        }
        else
        {
            LNode* p = this->List, * s;
            s = new LNode();
            if (s == NULL)
            {
                return false;
            }
            else
            {
                s->elem = elem;
                int i = 0;
                while (i < index)
                {
                    p = p->next;
                    i++;
                }
                s->next = p->next;
                p->next = s;
                this->length++;
                return true;
            }
        }
    }
    template <class T>
    bool SingleLinkedList<T>::ListDelete(int index)
    {
        if (index<0 || index>=this->length)
        {
            return false;
        }
        else
        {
            LNode* p = this->List, * del;
            int i = 0;
            while (i < index)
            {
                p = p->next;
                i++;
            }
            del = p->next;
            p->next = del->next;
            delete del;
            --this->length;
            return true;
        }
    }
    template <class T>
    void SingleLinkedList<T>::TraverseList()
    {
        LNode* p = this->List->next;
        while (p != NULL)
        {
            cout << p->elem << "\t";
            p = p->next;
        }
        cout << endl;
    }
    template <class T>
    class SingleLinkedListWithOutHeadNode{
    public:
        SingleLinkedListWithOutHeadNode():length(0){}
        void InitList();
        void DestroyList();
        void ClearList();
        bool ListEmpty();
        int ListLength();
        T GetElem(int index);
        int LocateElem(T elem);
        T PriorElem(T elem);
        T NextElem(T elem);
        bool addFirst(T elem);
        bool addAfter(T elem);
        bool ListInsert(int index,T elem);
        bool ListDelete(int index);
        void TraverseList();
    private:
        typedef struct Node{
            T elem;
            struct Node *next;
        }*LinkedList,LNode;
        LinkedList List;
        int length;
    };
    template <class T>
    void SingleLinkedListWithOutHeadNode<T>::InitList()
    {
        List=NULL;
    }
    template <class T>
    void SingleLinkedListWithOutHeadNode<T>::DestroyList()
    {
        LNode *p=this->List;
        while(this->List!=NULL)
        {
            p=this->List;
            this->List=p->next;
            delete p;
        }
        this->length=0;
    }
    template <class T>
    void SingleLinkedListWithOutHeadNode<T>::ClearList()
    {
        LNode *p=this->List;
        while(this->List!=NULL)
        {
            p=this->List;
            this->List=p->next;
            delete p;
        }
        this->length=0;
    }
    template <class T>
    bool SingleLinkedListWithOutHeadNode<T>::ListEmpty()
    {
        if(this->List!=NULL)
        {
            return false;
        }
        else
        {
            return true;
        }
    }
    template <class T>
    int SingleLinkedListWithOutHeadNode<T>::ListLength()
    {
        return this->length;
    }
    template <class T>
    T SingleLinkedListWithOutHeadNode<T>::GetElem(int index)
    {
        if(index<0||index>=this->length)
        {
            return NULL;
        }
        else
        {
            LNode *p=this->List;
            int counter=0;
            while(counter<index)
            {
                counter++;
                p=p->next;
            }
            return p->elem;
        }
    }
    template <class T>
    int SingleLinkedListWithOutHeadNode<T>::LocateElem(T elem)
    {
        LNode *p=this->List;
        int counter=0;
        while(counter<this->length&&p!=NULL)
        {
            if(p->elem==elem)
            {
                return counter;
            }
            p=p->next;
            counter++;
        }
        return -1;
    }
    template <class T>
    T SingleLinkedListWithOutHeadNode<T>::PriorElem(T elem)
    {
        LNode *p=this->List;
        while(p->next!=NULL)
        {
            if(p->next->elem==elem)
            {
                return p->elem;
            }
            p=p->next;
        }
        return NULL;
    }
    template <class T>
    T SingleLinkedListWithOutHeadNode<T>::NextElem(T elem)
    {
        LNode *p=this->List;
        while(p->next!=NULL)
        {
            if(p->elem==elem)
            {
                return p->next->elem;
            }
            p=p->next;
        }
        return NULL;
    }
    template <class T>
    bool SingleLinkedListWithOutHeadNode<T>::addFirst(T elem)
    {
        if(this->List==NULL)
        {
            this->List=new LNode();
            if(this->List==NULL)
            {
                return false;
            }
            else
            {
                this->List->elem=elem;
                this->List->next=NULL;
                ++this->length;
                return true;
            }
        }
        else
        {
            LNode *summon=new LNode();
            if(summon==NULL)
            {
                return false;
            }
            else
            {
                summon->elem=elem;
                summon->next=this->List;
                this->List=summon;
                ++this->length;
                return true;
            }
        }
    }
    template <class T>
    bool SingleLinkedListWithOutHeadNode<T>::addAfter(T elem)
    {
        if(this->List==NULL)
        {
            return this->addFirst(elem);
        }
        else
        {
            LNode *p=this->List;
            LNode *summon=new LNode();
            if(summon==NULL)
            {
                return false;
            }
            else
            {
                summon->elem=elem;
                while(p->next!=NULL)
                {
                    p=p->next;
                }
                summon->next=p->next;
                p->next=summon;
                ++this->length;
                return true;
            }
        }
    }
    template <class T>
    bool SingleLinkedListWithOutHeadNode<T>::ListInsert(int index,T elem)
    {
        if(index<0||index>this->length)
        {
            return false;
        }
        else
        {
            if(index==0)
            {
                return this->addFirst(elem);
            }
            else
            {
                LNode *p=this->List;
                LNode *summon=new LNode();
                if(summon==NULL)
                {
                    return false;
                }
                else
                {
                    summon->elem=elem;
                    int counter=1;
                    while(counter<index)
                    {
                        counter++;
                        p=p->next;
                    }
                    summon->next=p->next;
                    p->next=summon;
                    ++this->length;
                    return true;
                }
            }
        }
    }
    template <class T>
    bool SingleLinkedListWithOutHeadNode<T>::ListDelete(int index)
    {
        if(index<0||index>=this->length)
        {
            return false;
        }
        else
        {
            if(index==0)
            {
                LNode *temp=this->List;
                this->List=temp->next;
                temp->next=NULL;
                delete temp;
                --this->length;
                return true;
            }
            else
            {
                LNode *p=this->List,*del=NULL;
                int counter=1;
                while(counter<index)
                {
                    p=p->next;
                    counter++;
                }
                del=p->next;
                p->next=del->next;
                delete del;
                del=NULL;
                --this->length;
                return true;
            }
        }
    }
    template <class T>
    void SingleLinkedListWithOutHeadNode<T>::TraverseList()
    {
        LNode *p=this->List;
        while(p!=NULL)
        {
            cout<<p->elem<<"\t";
            p=p->next;
        }
        cout<<endl;
    }
    template <class T>
    class CircularSingleLinkedList
    {
    public:
        CircularSingleLinkedList():length(0){}
        bool InitList();
        void DestroyList();
        void ClearList();
        bool ListEmpty();
        int ListLength();
        T GetElem(int index);
        int LocateElem(T elem);
        T PriorElem(T elem);
        T NextElem(T elem);
        bool addFirst(T elem);
        bool addAfter(T elem);
        bool ListInsert(int index,T elem);
        bool ListDelete(int index);
        void TraverseList();
    private:
        typedef struct Node{
            T elem;
            struct Node *next;
        }*LinkedList,LNode;
        LinkedList List;
        int length;
    };
    template <class T>
    bool CircularSingleLinkedList<T>::InitList()
    {
        this->List=new LNode();
        if(this->List==NULL)
        {
            return false;
        }
        else
        {
            this->List->next=this->List;
            return true;
        }
    }
    template <class T>
    void CircularSingleLinkedList<T>::DestroyList()
    {
        LNode *p=this->List;
        while(this->List->next!=this->List)
        {
            p=this->List->next;
            this->List->next=p->next;
            delete p;
            p=NULL;
        }
        this->List=NULL;
        this->length=0;
    }
    template <class T>
    void CircularSingleLinkedList<T>::ClearList()
    {
        LNode *p=this->List;
        while(this->List->next!=this->List)
        {
            p=this->List->next;
            this->List->next=p->next;
            delete p;
            p=NULL;
        }
        this->List->next=this->List;
        this->length=0;
    }
    template <class T>
    bool CircularSingleLinkedList<T>::ListEmpty()
    {
        if(this->List->next==this->List)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    template <class T>
    int CircularSingleLinkedList<T>::ListLength()
    {
        return this->length;
    }
    template <class T>
    T CircularSingleLinkedList<T>::GetElem(int index)
    {
        if(index<0||index>=this->length)
        {
            return NULL;
        }
        else
        {
            LNode *p=this->List->next;
            int counter=0;
            while(counter<index)
            {
                counter++;
                p=p->next;
            }
            return p->elem;
        }
    }
    template <class T>
    int CircularSingleLinkedList<T>::LocateElem(T elem)
    {
        LNode *p=this->List->next;
        int counter=0;
        int result=-1;
        while(counter<this->length)
        {
            if(p->elem==elem)
            {
                result=counter;
                break;
            }
            p=p->next;
            counter++;
        }
        return result;
    }
    template <class T>
    T CircularSingleLinkedList<T>::PriorElem(T elem)
    {
        LNode *p=this->List->next;
        while(p!=this->List)
        {
            if(p->next->elem==elem)
            {
                return p->elem;
            }
            else if(this->LocateElem(elem)==0)
            {
                while(p->next!=this->List)
                {
                    p=p->next;
                }
                return p->elem;
            }
            p=p->next;
        }
        return NULL;
    }
    template <class T>
    T CircularSingleLinkedList<T>::NextElem(T elem)
    {
        LNode *p=this->List->next;
        while(p!=this->List)
        {
            if(p->elem==elem)
            {
                if(ListLength()==(LocateElem(elem)+1))
                {
                    return p->next->next->elem;
                }
                else
                {
                    return p->next->elem;
                }
            }
            p=p->next;
        }
        return NULL;
    }
    template <class T>
    bool CircularSingleLinkedList<T>::addFirst(T elem)
    {
        LNode *summon,*p=this->List;
        summon=new LNode();
        if(summon==NULL)
        {
            return false;
        }
        else
        {
            summon->elem=elem;
            summon->next=p->next;
            p->next=summon;
            ++this->length;
            return true;
        }
    }
    template <class T>
    bool CircularSingleLinkedList<T>::addAfter(T elem)
    {
        LNode *summon,*p=this->List;
        summon=new LNode();
        if(summon==NULL)
        {
            return false;
        }
        else
        {
            summon->elem=elem;
            while(p->next!=this->List)
            {
                p=p->next;
            }
            summon->next=p->next;
            p->next=summon;
            ++this->length;
            return true;
        }
    }
    template <class T>
    bool CircularSingleLinkedList<T>::ListInsert(int index,T elem)
    {
        if(index<0||index>this->length)
        {
            return false;
        }
        else
        {
            LNode *p=this->List,*summon;
            summon=new LNode();
            if(summon==NULL)
            {
                return false;
            }
            else
            {
                summon->elem=elem;
                int counter=0;
                while(counter<index)
                {
                    p=p->next;
                    counter++;
                }
                summon->next=p->next;
                p->next=summon;
                ++this->length;
                return true;
            }
        }
    }
    template <class T>
    bool CircularSingleLinkedList<T>::ListDelete(int index)
    {
        if(index<0||index>=this->length)
        {
            return false;
        }
        else
        {
            LNode *p=this->List,*del;
            int counter=0;
            while(counter<index)
            {
                p=p->next;
                counter++;
            }
            del=p->next;
            p->next=del->next;
            delete del;
            del=NULL;
            --this->length;
            return true;
        }
    }
    template <class T>
    void CircularSingleLinkedList<T>::TraverseList()
    {
        LNode *p=this->List->next;
        while(p!=this->List)
        {
            cout<<p->elem<<"\t";
            p=p->next;
        }
        cout<<endl;
    }
    template <class T>
    class DoubleLinkedList{
    public:
        DoubleLinkedList():length(0),List(NULL){}
        bool InitList();
        void DestroyList();
        void ClearList();
        bool ListEmpty();
        int ListLength();
        T GetElem(int index);
        int LocateElem(T elem);
        T PriorElem(T elem);
        T NextElem(T elem);
        bool addFirst(T elem);
        bool addAfter(T elem);
        bool ListInsert(int index,T elem);
        bool ListDelete(int index);
        void TraverseList();
        void TraverseListByReverseOrder();
    private:
        typedef struct Node{
            T elem;
            struct Node *prior;
            struct Node *next;
        }LNode,*LinkedList;
        LinkedList List;
        int length;
    };
    template <class T>
    bool DoubleLinkedList<T>::InitList()
    {
        this->List=new LNode();
        if(this->List==NULL)
        {
            return false;
        }
        else
        {
            this->List->elem=NULL;
            this->List->next=NULL;
            this->List->prior=NULL;
            return true;
        }
    }
    template <class T>
    void DoubleLinkedList<T>::DestroyList()
    {
        LNode *p=this->List;
        while(this->List!=NULL)
        {
            p=this->List;
            this->List=p->next;
            delete p;
            p=NULL;
        }
        this->length=0;
    }
    template <class T>
    void DoubleLinkedList<T>::ClearList()
    {
        LNode *p=this->List;
        while(this->List->next!=NULL)
        {
            p=this->List->next;
            this->List->next=p->next;
            delete p;
            p=NULL;
        }
        this->length=0;
    }
    template <class T>
    bool DoubleLinkedList<T>::ListEmpty()
    {
        if(this->List->next!=NULL)
        {
            return false;
        }
        else
        {
            return true;
        }
    }
    template <class T>
    int DoubleLinkedList<T>::ListLength()
    {
        return this->length;
    }
    template <class T>
    T DoubleLinkedList<T>::GetElem(int index)
    {
        if(index<0||index>=this->length)
        {
            return NULL;
        }else
        {
            LNode *p=this->List->next;
            int counter=0;
            while(counter<index)
            {
                p=p->next;
                counter++;
            }
            return p->elem;
        }
    }
    template <class T>
    int DoubleLinkedList<T>::LocateElem(T elem)
    {
        LNode *p=this->List->next;
        int counter=0;
        while(counter<this->length&&p!=NULL)
        {
            if(p->elem==elem)
            {
                return counter;
            }
            p=p->next;
            counter++;
        }
        return -1;
    }
    template <class T>
    T DoubleLinkedList<T>::PriorElem(T elem)
    {
        LNode *p=this->List->next;
        while(p!=NULL)
        {
            if(p->elem==elem&&this->LocateElem(elem)!=0)
            {
                return p->prior->elem;
            }
            p=p->next;
        }
        return NULL;
    }
    template <class T>
    T DoubleLinkedList<T>::NextElem(T elem)
    {
        LNode *p=this->List->next;
        while(p!=NULL)
        {
            if(p->elem==elem&&this->LocateElem(elem)!=this->length-1)
            {
                return p->next->elem;
            }
            p=p->next;
        }
        return NULL;
    }
    template <class T>
    bool DoubleLinkedList<T>::addFirst(T elem)
    {
        LNode *p=this->List,*summon;
        summon=new LNode();
        if(summon==NULL)
        {
            return false;
        }
        else{
            summon->elem=elem;
            summon->next=p->next;
            p->next=summon;
            summon->prior=p;
            if(summon->next!=NULL)
            {
                summon->next->prior=summon;
            }
            ++this->length;
            return true;
        }
    }
    template <class T>
    bool DoubleLinkedList<T>::addAfter(T elem)
    {
        LNode *p=this->List,*summon;
        while(p->next!=NULL)
        {
            p=p->next;
        }
        summon=new LNode();
        if(summon!=NULL)
        {
            summon->elem=elem;
            summon->next=p->next;
            summon->prior=p;
            p->next=summon;
            ++this->length;
            return true;
        }
        else
        {
            return false;
        }
    }
    template <class T>
    bool DoubleLinkedList<T>::ListInsert(int index,T elem)
    {
        if(index<0||index>this->length)
        {
            return false;
        }
        else if(index==0)
        {
            return this->addFirst(elem);
        }
        else
        {
            LNode *p=this->List,*summon;
            int counter=0;
            while(counter<index)
            {
                p=p->next;
                counter++;
            }
            summon=new LNode();
            if(summon!=NULL)
            {
                summon->elem=elem;
                summon->next=p->next;
                summon->prior=p;
                p->next=summon;
                if(summon->next!=NULL)
                {
                    summon->next->prior=summon;
                }
                ++this->length;
                return true;
            }
            else
            {
                return false;
            }
        }
    }
    template <class T>
    bool DoubleLinkedList<T>::ListDelete(int index)
    {
        if(index<0||index>=this->length)
        {
            return false;
        }
        else if(index==this->length-1)
        {
            LNode *p=this->List,*del;
            int counter=0;
            while(counter<index)
            {
                p=p->next;
                counter++;
            }
            del=p->next;
            del->prior->next=NULL;
            del->prior=NULL;
            delete del;
            --this->length;
            return true;
        }
        else
        {
            LNode *p=this->List,*del;
            int counter=0;
            while(counter<index)
            {
                p=p->next;
                counter++;
            }
            del=p->next;
            del->prior->next=del->next;
            del->next->prior=del->prior;
            delete del;
            --this->length;
            return true;
        }
    }
    template <class T>
    void DoubleLinkedList<T>::TraverseList()
    {
        LNode *p=this->List->next;
        while(p!=NULL)
        {
            cout<<p->elem<<"\t";
            p=p->next;
        }
        cout<<endl;
    }
    template <class T>
    void DoubleLinkedList<T>::TraverseListByReverseOrder()
    {
        if(this->ListEmpty())
        {
            cout<<endl;
        }else
        {
            LNode *p=this->List->next;
            while(p->next!=NULL)
            {
                p=p->next;
            }
            while(p->prior!=NULL)
            {
                cout<<p->elem<<"\t";
                p=p->prior;
            }
            cout<<endl;
        }
    }
    template <class T>
    class DoubleLinkedListWithoutHeadNode
    {
    public:
        DoubleLinkedListWithoutHeadNode():length(0),List(NULL){}
        void InitList();
        void DestroyList();
        void ClearList();
        bool ListEmpty();
        int ListLength();
        T GetElem(int index);
        int LocateElem(T elem);
        T PriorElem(T elem);
        T NextElem(T elem);
        bool addFirst(T elem);
        bool addAfter(T elem);
        bool ListInsert(int index,T elem);
        bool ListDelete(int index);
        void TraverseList();
        void TraverseListByReverseOrder();
    private:
        typedef struct Node
        {
            T elem;
            struct Node *prior;
            struct Node *next;
        }LNode,*LinkedList;
        LinkedList List;
        int length;
    };
    template <class T>
    void DoubleLinkedListWithoutHeadNode<T>::InitList()
    {
        this->List=NULL;
    }
    template <class T>
    void DoubleLinkedListWithoutHeadNode<T>::DestroyList()
    {
        LNode *p=this->List;
        if(p!=NULL)
        {
            this->List=p->next;
            this->DestroyList();
            delete p;
            --this->length;
            p=NULL;
        }
    }
    template <class T>
    void DoubleLinkedListWithoutHeadNode<T>::ClearList()
    {
        LNode *p=this->List;
        if(p!=NULL)
        {
            this->List=p->next;
            this->DestroyList();
            delete p;
            --this->length;
            p=NULL;
        }
    }
    template <class T>
    bool DoubleLinkedListWithoutHeadNode<T>::ListEmpty()
    {
        if(this->List==NULL)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    template <class T>
    int DoubleLinkedListWithoutHeadNode<T>::ListLength()
    {
        return this->length;
    }
    template <class T>
    T DoubleLinkedListWithoutHeadNode<T>::GetElem(int index)
    {
        if(index<0||index>=this->length)
        {
            return NULL;
        }else
        {
            int counter=0;
            LNode *p=this->List;
            while(counter<index)
            {
                p=p->next;
                counter++;
            }
            return p->elem;
        }
    }
    template <class T>
    int DoubleLinkedListWithoutHeadNode<T>::LocateElem(T elem)
    {
        LNode *p=this->List;
        int counter=0;
        while(p!=NULL)
        {
            if(p->elem==elem)
            {
                return counter;
            }
            counter++;
            p=p->next;
        }
        return -1;
    }
    template <class T>
    T DoubleLinkedListWithoutHeadNode<T>::PriorElem(T elem)
    {
        LNode *p=this->List;
        while(p!=NULL)
        {
            if(p->elem==elem)
            {
                if(p->prior==NULL)
                {
                    break;
                }
                return p->prior->elem;
            }
            p=p->next;
        }
        return NULL;
    }
    template <class T>
    T DoubleLinkedListWithoutHeadNode<T>::NextElem(T elem)
    {
        LNode *p=this->List;
        while(p!=NULL)
        {
            if(p->elem==elem)
            {
                if(p->next==NULL)
                {
                    break;
                }
                return p->next->elem;
            }
            p=p->next;
        }
        return NULL;
    }
    template <class T>
    bool DoubleLinkedListWithoutHeadNode<T>::addFirst(T elem)
    {
        if(this->List==NULL)
        {
            this->List=new LNode();
            if(this->List==NULL)
            {
                return false;
            }
            else
            {
                this->List->elem=elem;
                this->List->prior=NULL;
                this->List->next=NULL;
                ++this->length;
                return true;
            }
        }
        else
        {
            LNode *summon=new LNode();
            if(summon==NULL)
            {
                return false;
            }
            else
            {
                summon->elem=elem;
                summon->next=this->List;
                summon->prior=NULL;
                this->List->prior=summon;
                this->List=summon;
                ++this->length;
                return true;
            }
        }
    }
    template <class T>
    bool DoubleLinkedListWithoutHeadNode<T>::addAfter(T elem)
    {
        if(this->List==NULL)
        {
            this->List=new LNode();
            if(this->List==NULL)
            {
                return false;
            }
            else
            {
                this->List->elem=elem;
                this->List->next=NULL;
                this->List->prior=NULL;
                ++this->length;
                return true;
            }
        }
        else
        {
            LNode *p=this->List,*summon;
            summon=new LNode();
            if(summon==NULL)
            {
                return false;
            }
            else
            {
                summon->elem=elem;
                while(p->next!=NULL)
                {
                    p=p->next;
                }
                summon->next=p->next;
                p->next=summon;
                summon->prior=p;
                ++this->length;
                return true;
            }
        }
    }
    template <class T>
    bool DoubleLinkedListWithoutHeadNode<T>::ListInsert(int index,T elem)
    {
        if(index<0||index>this->length)
        {
            return false;
        }
        else if(index==0)
        {
            return this->addFirst(elem);
        }
        else if(index==this->length)
        {
            return this->addAfter(elem);
        }
        else
        {
            LNode *p=this->List,*summon;
            int counter=1;
            summon=new LNode();
            if(summon==NULL)
            {
                return false;
            }
            else
            {
                summon->elem=elem;
                while(counter<index)
                {
                    counter++;
                    p=p->next;
                }
                summon->next=p->next;
                p->next->prior=summon;
                summon->prior=p;
                p->next=summon;
                ++this->length;
                return true;
            }
        }
    }
    template <class T>
    bool DoubleLinkedListWithoutHeadNode<T>::ListDelete(int index)
    {
        if(index<0||index>=this->length)
        {
            return false;
        }
        else if(index==0)
        {
            if(this->length==1)
            {
                delete this->List;
                this->List=NULL;
                this->length=0;
                return true;
            }else
            {
                LNode *del=this->List;
                this->List=del->next;
                del->next=NULL;
                del->prior=NULL;
                delete del;
                del=NULL;
                this->List->prior=NULL;
                --this->length;
                return true;
            }
        }
        else
        {
            int counter=0;
            LNode *p=this->List,*del;
            while(counter<index&&p->next!=NULL)
            {
                p=p->next;
                counter++;
            }
            del=p;
            if(del->next!=NULL)
            {
                del->next->prior=del->prior;
                del->prior->next=del->next;
                delete del;
                del=NULL;
                --this->length;
                return true;
            }
            else
            {
                del->prior->next=NULL;
                del->prior=NULL;
                delete del;
                del=NULL;
                --this->length;
                return true;
            }
        }
    }
    template <class T>
    void DoubleLinkedListWithoutHeadNode<T>::TraverseList()
    {
        LNode *p=this->List;
        while(p!=NULL)
        {
            cout<<p->elem<<"\t";
            p=p->next;
        }
        cout<<endl;
    }
    template <class T>
    void DoubleLinkedListWithoutHeadNode<T>::TraverseListByReverseOrder()
    {
        if(this->ListEmpty())
        {
            cout<<endl;
        }else
        {
            LNode *p=this->List;
            while(p->next!=NULL)
            {
                p=p->next;
            }
            while(p!=NULL)
            {
                cout<<p->elem<<"\t";
                p=p->prior;
            }
            cout<<endl;
        }
    }
    template <class T>
    class CircularDoubleLinkedList
    {
    public:
        CircularDoubleLinkedList():List(NULL),length(0){}
        bool InitList();
        void DestroyList();
        void ClearList();
        bool ListEmpty();
        int ListLength();
        T GetElem(int index);
        int LocateElem(T elem);
        T PriorElem(T elem);
        T NextElem(T elem);
        bool addFirst(T elem);
        bool addAfter(T elem);
        bool ListInsert(int index,T elem);
        bool ListDelete(int index);
        void TraverseList();
        void TraverseListByReverseOrder();
    private:
        typedef struct Node
        {
            T elem;
            struct Node *prior;
            struct Node *next;
        }LNode,*LinkedList;
        LinkedList List;
        int length;
    };
    template <class T>
    bool CircularDoubleLinkedList<T>::InitList()
    {
        this->List=new LNode();
        if(this->List==NULL)
        {
            return false;
        }else
        {
            this->List->elem=NULL;
            this->List->next=this->List;
            this->List->prior=this->List;
            return true;
        }
    }
    template <class T>
    void CircularDoubleLinkedList<T>::DestroyList()
    {
        LNode *p=this->List,*del;
        while(p!=this->List)
        {
            p=p->next;
        }
        while(p!=this->List)
        {
            del=p;
            p=del->prior;
            del->prior->next=del->next;
            del->next->prior=del->prior;
            delete del;
            del=NULL;
        }
        delete this->List;
        this->List=NULL;
        this->length=0;
    }
    template <class T>
    void CircularDoubleLinkedList<T>::ClearList()
    {
        LNode *p=this->List,*del;
        while(p->next!=this->List)
        {
            p=p->next;
        }
        while(p!=this->List)
        {
            del=p;
            p=del->prior;
            del->prior->next=del->next;
            del->next->prior=del->prior;
            delete del;
            del=NULL;
        }
        this->length=0;
    }
    template <class T>
    bool CircularDoubleLinkedList<T>::ListEmpty()
    {
        if(this->List->next==this->List)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    template <class T>
    int CircularDoubleLinkedList<T>::ListLength()
    {
        return this->length;
    }
    template <class T>
    T CircularDoubleLinkedList<T>::GetElem(int index)
    {
        if(index<0||index>=this->length)
        {
            return NULL;
        }
        else
        {
            int counter=0;
            LNode *p=this->List->next;
            while(counter<index)
            {
                counter++;
                p=p->next;
            }
            return p->elem;
        }
    }
    template <class T>
    int CircularDoubleLinkedList<T>::LocateElem(T elem)
    {
        int counter=0;
        LNode *p=this->List->next;
        while(p!=this->List)
        {
            if(p->elem==elem)
            {
                return counter;
            }
            counter++;
            p=p->next;
        }
        return -1;
    }
    template <class T>
    T CircularDoubleLinkedList<T>::PriorElem(T elem)
    {
        LNode *p=this->List->next;
        while(p!=this->List)
        {
            if(p->elem==elem)
            {
                if(this->LocateElem(elem)==0)
                {
                    return p->prior->prior->elem;
                }
                return p->prior->elem;
            }
            p=p->next;
        }
        return NULL;
    }
    template <class T>
    T CircularDoubleLinkedList<T>::NextElem(T elem)
    {
        LNode *p=this->List->next;
        while(p!=this->List)
        {
            if(p->elem==elem)
            {
                if(LocateElem(elem)==this->length-1)
                {
                    return p->next->next->elem;
                }
                return p->next->elem;
            }
            p=p->next;
        }
        return NULL;
    }
    template <class T>
    bool CircularDoubleLinkedList<T>::addFirst(T elem)
    {
        LNode *summon,*p=this->List;
        summon=new LNode();
        if(summon==NULL)
        {
            return false;
        }
        else
        {
            summon->elem=elem;
            summon->next=p->next;
            summon->next->prior=summon;
            summon->prior=p;
            p->next=summon;
            ++this->length;
            return true;
        }
    }
    template <class T>
    bool CircularDoubleLinkedList<T>::addAfter(T elem)
    {
        LNode *p=this->List,*summon;
        summon=new LNode();
        if(summon==NULL)
        {
            return false;
        }
        else
        {
            summon->elem=elem;
            summon->next=p;
            summon->prior=p->prior;
            summon->prior->next=summon;
            p->prior=summon;
            ++this->length;
            return true;
        }
    }
    template <class T>
    bool CircularDoubleLinkedList<T>::ListInsert(int index,T elem)
    {
        if(index<0||index>this->length)
        {
            return false;
        }else
        {
            LNode *p=this->List,*summon;
            summon=new LNode();
            if(summon==NULL)
            {
                return false;
            }
            else
            {
                summon->elem=elem;
                int counter=0;
                while(counter<index)
                {
                    p=p->next;
                    counter++;
                }
                summon->next=p->next;
                summon->next->prior=summon;
                summon->prior=p;
                summon->prior->next=summon;
                ++this->length;
                return true;
            }
        }
    }
    template <class T>
    bool CircularDoubleLinkedList<T>::ListDelete(int index)
    {
        if(index<0||index>=this->length)
        {
            return false;
        }
        else
        {
            int counter=0;
            LNode *p=this->List->next,*del;
            while(counter<index)
            {
                p=p->next;
                counter++;
            }
            del=p;
            del->prior->next=del->next;
            del->next->prior=del->prior;
            delete del;
            del=NULL;
            --this->length;
            return true;
        }
    }
    template <class T>
    void CircularDoubleLinkedList<T>::TraverseList()
    {
        LNode *p=this->List->next;
        while(p!=this->List)
        {
            cout<<p->elem<<"\t";
            p=p->next;
        }
        cout<<endl;
    }
    template <class T>
    void CircularDoubleLinkedList<T>::TraverseListByReverseOrder()
    {
        LNode *p=this->List->prior;
        while(p!=this->List)
        {
            cout<<p->elem<<"\t";
            p=p->prior;
        }
        cout<<endl;
    }
    template <class T>
    class SequentialStack
    {
    public:
        SequentialStack();
        bool InitStack(int length);
        void DestroyStack();
        void ClearStack();
        bool StackEmpty();
        int StackLength();
        T GetTop();
        bool Push(T elem);
        T Pop();
        void StackTraverse();
    private:
        typedef struct {
            T* base;
            T* top;
            int stacksize;
        }SqStack;
        SqStack stack;
    };
    template <class T>
    SequentialStack<T>::SequentialStack()
    {
        this->stack.base=NULL;
        this->stack.top = NULL;
        this->stack.stacksize = NULL;
    }
    template <class T>
    bool SequentialStack<T>::InitStack(int length)
    {
        stack.base = new T[length];
        stack.top = stack.base;
        if (stack.base != NULL && stack.top != NULL)
        {
            stack.stacksize = length;
            return true;
        }
        else
        {
            return false;
        }
    }
    template <class T>
    void SequentialStack<T>::DestroyStack()
    {
        delete[]stack.base;
        stack.base = NULL;
        stack.top = NULL;
        stack.stacksize = NULL;
    }
    template <class T>
    void SequentialStack<T>::ClearStack()
    {
        for (int i=0;i<stack.stacksize;i++)
        {
            stack.base[i] = NULL;
        }
        stack.top = stack.base;
    }
    template <class T>
    bool SequentialStack<T>::StackEmpty()
    {
        if (stack.base == stack.top)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    template <class T>
    int SequentialStack<T>::StackLength()
    {
        return stack.top - stack.base;
    }
    template <class T>
    T SequentialStack<T>::GetTop()
    {
        if (stack.top != stack.base)
        {
            return *(stack.top-1);
        }
        else
        {
            return NULL;
        }
    }
    template <class T>
    bool SequentialStack<T>::Push(T elem)
    {
        if (((stack.top)-(stack.base))==stack.stacksize)
        {
            return false;
        }
        else
        {
            stack.top[0] = elem;
            ++stack.top;
            return true;
        }
    }
    template <class T>
    T SequentialStack<T>::Pop()
    {
        if (stack.top==stack.base)
        {
            return NULL;
        }
        else
        {
            --stack.top;
            return stack.top[0];
        }
    }
    template <class T>
    void SequentialStack<T>::StackTraverse()
    {
        int counter = 0;
        while (counter<((stack.top)-(stack.base)))
        {
            cout << stack.base[counter] << "\t";
            counter++;
        }
        cout << endl;
    }
    template <class T>
    class LinkedStack
    {
    public:
        LinkedStack(int length) :stack_length(length),Stack(NULL){}
        bool InitStack();
        void DestroyStack();
        void ClearStack();
        bool StackEmpty();
        int StackLength();
        T GetTop();
        bool Push(T elem);
        T Pop();
        void StackTraverse();
    private:
        typedef struct Node
        {
            T elem;
            struct Node* next;
        }StackNode,*Linkedstack;
        int stack_length;
        Linkedstack Stack;
    };
    template <class T>
    bool LinkedStack<T>::InitStack()
    {
        this->Stack = new StackNode();
        if (this->Stack!= NULL)
        {
            this->Stack->elem = this->stack_length;
            this->Stack->next = NULL;
            return true;
        }
        else
        {
            return false;
        }
    }
    template <class T>
    void LinkedStack<T>::DestroyStack()
    {
        StackNode* pointer = this->Stack;
        while (this->Stack!=NULL)
        {
            pointer = this->Stack;
            this->Stack = pointer->next;
            delete pointer;
            pointer = NULL;
        }
    }
    template <class T>
    void LinkedStack<T>::ClearStack()
    {
        StackNode* pointer = this->Stack->next;
        while (this->Stack->next!= NULL)
        {
            pointer = this->Stack->next;
            this->Stack->next= pointer->next;
            delete pointer;
            pointer = NULL;
        }
    }
    template <class T>
    bool LinkedStack<T>::StackEmpty()
    {
        if (this->Stack->next == NULL)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    template <class T>
    int LinkedStack<T>::StackLength()
    {
        StackNode* pointer = this->Stack;
        int counter = 0;
        while (counter<this->Stack->elem&&pointer->next!=NULL)
        {
            counter++;
            pointer=pointer->next;
        }
        return counter;
    }
    template <class T>
    T LinkedStack<T>::GetTop()
    {
        if (this->Stack->next != NULL)
        {
            return this->Stack->next->elem;
        }
        else
        {
            return NULL;
        }
    }
    template <class T>
    bool LinkedStack<T>::Push(T elem)
    {
        if (this->StackLength() == this->Stack->elem)
        {
            return false;
        }
        else
        {
            StackNode* summon = new StackNode();
            summon->elem = elem;
            summon->next = this->Stack->next;
            this->Stack->next = summon;
            return true;
        }
    }
    template <class T>
    T LinkedStack<T>::Pop()
    {
        if (this->Stack->next == NULL)
        {
            return NULL;
        }
        else
        {
            StackNode* pointer = this->Stack->next;
            this->Stack->next = pointer->next;
            T data_temp = pointer->elem;
            delete pointer;
            pointer = NULL;
            return data_temp;
        }
    }
    template <class T>
    void LinkedStack<T>::StackTraverse()
    {
        StackNode* pointer = this->Stack->next;
        while (pointer!=NULL)
        {
            cout << pointer->elem << "\t";
            pointer = pointer->next;
        }
        cout << endl;
    }
    template <class T>
    class SequentialQueue
    {
    public:
        SequentialQueue(int max_size) :size(max_size) {
            Queue.base = NULL;
        }
        bool InitQueue();
        void DestroyQueue();
        void ClearQueue();
        bool QueueEmpty();
        int QueueLength();
        T GetHead();
        bool EnQueue(T elem);
        T DeQueue();
        void QueueTraverse();
    private:
        typedef struct Node
        {
            T* base;
            int front;
            int rear;
            int size;
        }SqQueue;
        SqQueue Queue;
        int size;
    };
    template <class T>
    bool SequentialQueue<T>::InitQueue()
    {
        this->Queue.base = new T[this->size];
        if (this->Queue.base!=NULL)
        {
            this->Queue.size = this->size;
            this->Queue.front = this->Queue.rear = 0;
            return true;
        }
        else
        {
            return false;
        }
    }
    template <class T>
    void SequentialQueue<T>::DestroyQueue()
    {
        delete[]this->Queue.base;
        this->Queue.base = NULL;
        this->Queue.front = this->Queue.rear = NULL;
        this->Queue.size =NULL;
    }
    template <class T>
    void SequentialQueue<T>::ClearQueue()
    {
        for (int i=0;i<this->Queue.size;i++)
        {
            *(this->Queue.base + i) = NULL;
        }
        Queue.front = Queue.rear = 0;
    }
    template <class T>
    bool SequentialQueue<T>::QueueEmpty()
    {
        if (Queue.front==Queue.rear)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    template <class T>
    int SequentialQueue<T>::QueueLength()
    {
        return (Queue.rear) - (Queue.front);
    }
    template <class T>
    T SequentialQueue<T>::GetHead()
    {
        if (this->QueueEmpty())
        {
            return NULL;
        }
        else
        {
            return Queue.base[Queue.front];
        }
    }
    template <class T>
    bool SequentialQueue<T>::EnQueue(T elem)
    {
        if (this->QueueLength()==Queue.size)
        {
            return false;
        }
        else
        {
            Queue.base[Queue.rear++] = elem;
            return true;
        }
    }
    template <class T>
    T SequentialQueue<T>::DeQueue()
    {
        if (QueueEmpty())
        {
            return NULL;
        }
        else
        {
            T data_temp = Queue.base[Queue.front++];
            return data_temp;
        }
    }
    template <class T>
    void SequentialQueue<T>::QueueTraverse()
    {
        int counter = Queue.front;
        while (counter<Queue.rear)
        {
            cout << Queue.base[counter] << "\t";
            counter++;
        }
        cout << endl;
    }
    template <class T>
    class CircularQueue
    {
    public:
        CircularQueue(int maxium_size):max_size(maxium_size){}
        bool InitQueue();
        void DestroyQueue();
        void ClearQueue();
        bool QueueEmpty();
        int QueueLength();
        T GetHead();
        bool EnQueue(T elem);
        T DeQueue();
        void QueueTraverse();
    private:
        typedef struct Node{
            T *base;
            int q_front;
            int q_rear;
            int q_size;
            int tag;
        }SqQueue;
        SqQueue Queue;
        int max_size;
    };
    template <class T>
    bool CircularQueue<T>::InitQueue()
    {
        this->Queue.base=new T[this->max_size];
        if(Queue.base!=NULL)
        {
            for(int i=0;i<max_size;i++)
            {
                Queue.base[i]=NULL;
            }
            Queue.q_front=0;
            Queue.q_rear=0;
            Queue.q_size=max_size;
            Queue.tag=0;
            return true;
        }else{
            return false;
        }
    }
    template <class T>
    void CircularQueue<T>::DestroyQueue()
    {
        delete []Queue.base;
        Queue.base=NULL;
        Queue.q_front=NULL;
        Queue.q_rear=NULL;
        Queue.q_size=NULL;
    }
    template <class T>
    void CircularQueue<T>::ClearQueue()
    {
        for(int i=0;i<Queue.q_size;i++)
        {
            *(Queue.base+i)=NULL;
        }
        Queue.q_front=0;
        Queue.q_rear=0;
        Queue.tag=0;
    }
    template <class T>
    bool CircularQueue<T>::QueueEmpty()
    {
        if(Queue.q_front%Queue.q_size==Queue.q_rear%Queue.q_size&&Queue.tag==0)
        {
            return true;
        }else
        {
            return false;
        }
    }
    template <class T>
    int CircularQueue<T>::QueueLength()
    {
        return Queue.q_rear-Queue.q_front;
    }
    template <class T>
    T CircularQueue<T>::GetHead()
    {
        if(this->QueueEmpty())
        {
            return false;
        }else
        {
            return true;
        }
    }
    template <class T>
    bool CircularQueue<T>::EnQueue(T elem)
    {
        if(Queue.q_front%Queue.q_size==Queue.q_rear%Queue.q_size&&Queue.tag==1)
        {
            return false;
        }else
        {
            Queue.base[Queue.q_rear%Queue.q_size]=elem;
            ++Queue.q_rear;
            Queue.tag=1;
            return true;
        }
    }
    template <class T>
    T CircularQueue<T>::DeQueue()
    {
        if(Queue.q_front%Queue.q_size==Queue.q_rear%Queue.q_size&&Queue.tag==0)
        {
            return false;
        }else
        {
            T temp=Queue.base[Queue.q_front%Queue.q_size];
            Queue.base[Queue.q_front%Queue.q_size]=NULL;
            ++Queue.q_front;
            Queue.tag=0;
            return temp;
        }
    }
    template <class T>
    void CircularQueue<T>::QueueTraverse()
    {
        int counter=0;
        while(counter<Queue.q_size)
        {
            if(Queue.base[counter]==NULL)
            {
                counter++;
                continue;
            }else
            {
                cout<<Queue.base[counter]<<"\t";
                counter++;
            }
        }
        cout<<endl;
    }
    template <class T>
    class LinkedQueue
    {
    public:
        LinkedQueue(){}
        bool InitQueue();
        void DestroyQueue();
        void ClearQueue();
        bool QueueEmpty();
        int QueueLength();
        T GetHead();
        bool EnQueue(T elem);
        T DeQueue();
        void QueueTraverse();
    private:
        typedef struct Node
        {
            T elem;
            struct Node *next;
        }QNode,*QueuePtr;
        typedef struct
        {
            QueuePtr q_front;
            QueuePtr q_rear;
        }LQueue;
        LQueue Queue;
    };
    template <class T>
    bool LinkedQueue<T>::InitQueue()
    {
        Queue.q_front=new QNode();
        if(Queue.q_front!=NULL)
        {
            Queue.q_front->elem=0;
            Queue.q_front->next=NULL;
            Queue.q_rear=Queue.q_front;
            return true;
        }else
        {
            return false;
        }
    }
    template <class T>
    void LinkedQueue<T>::DestroyQueue()
    {
        QNode *pointer=Queue.q_front;
        while(Queue.q_front!=NULL)
        {
            pointer=Queue.q_front;
            Queue.q_front=pointer->next;
            delete pointer;
            pointer=NULL;
        }
    }
    template <class T>
    void LinkedQueue<T>::ClearQueue()
    {
        QNode *pointer=Queue.q_front;
        while(Queue.q_front->next!=NULL)
        {
            pointer=Queue.q_front->next;
            Queue.q_front->next=pointer->next;
            delete pointer;
            pointer=NULL;
        }
        Queue.q_rear=Queue.q_front;
    }
    template <class T>
    bool LinkedQueue<T>::QueueEmpty()
    {
        if(Queue.q_front->next==NULL)
        {
            return true;
        }else
        {
            return false;
        }
    }
    template <class T>
    int LinkedQueue<T>::QueueLength()
    {
        QNode *pointer=Queue.q_front;
        int counter=0;
        while(pointer->next!=NULL)
        {
            counter++;
            pointer=pointer->next;
        }
        return counter;
    }
    template <class T>
    T LinkedQueue<T>::GetHead()
    {
        if(Queue.q_front==Queue.q_rear)
        {
            return NULL;
        }else
        {
            return Queue.q_front->next->elem;
        }
    }
    template <class T>
    bool LinkedQueue<T>::EnQueue(T elem)
    {
        QNode *summon=new QNode();
        if(summon==NULL)
        {
            return false;
        }else
        {
            summon->elem=elem;
            summon->next=Queue.q_rear->next;
            Queue.q_rear->next=summon;
            Queue.q_rear=summon;
            return true;
        }
    }
    template <class T>
    T LinkedQueue<T>::DeQueue()
    {
        if(Queue.q_front==Queue.q_rear)
        {
            return NULL;
        }else
        {
            QNode *del=Queue.q_front->next;
            T temp=del->elem;
            if(del->next!=NULL)
            {
                Queue.q_front->next=del->next;
            }else
            {
                Queue.q_front->next=NULL;
                Queue.q_front=Queue.q_rear;
            }
            return temp;
        }
    }
    template <class T>
    void LinkedQueue<T>::QueueTraverse()
    {
        QNode *pointer=Queue.q_front;
        while(pointer->next!=NULL)
        {
            cout<<pointer->next->elem<<"\t";
            pointer=pointer->next;
        }
        cout<<endl;
    }
    class SequentialString
    {
    public:
        SequentialString(){String.ch=NULL;String.length=0;}
        bool StrAssign(char *chars);
        void StrCopy(char *chars);
        bool StrEmpty();
        int StrCompare(char *chars);
        int StrLength();
        void ClearString();
        bool Concat(char *chars);
        char* SubString(int position,int str_length);
        int Index_By_BF(char *chars,int position);
        int Index_By_KMP(char *chars,int position);
        void Replace_By_BF(char *old_str,char *new_str);
        void Replace_By_KMP(char *old_str,char *new_str);
        bool StrInsert(int position,char *chars);
        bool StrDelete(int position,int str_length);
        void DestroyString();
        char* GetString();
    private:
        typedef struct
        {
            char *ch;
            int length;
        }HString;
        HString String;
    };
    bool SequentialString::StrAssign(char *chars)
    {
        int counter=0,i=0;
        while(chars[counter]!='\0')
        {
            counter++;
        }
        String.ch=new char[counter];
        if(String.ch!=NULL)
        {
            while(chars[i]!='\0')
            {
                String.ch[i]=chars[i];
                i++;
            }
            String.ch[i]='\0';
            String.length=counter;
            return true;
        }else
        {
            return false;
        }
    }
    void SequentialString::StrCopy(char *chars)
    {
        int counter=0;
        while(chars[counter]!='\0')
        {
            ++counter;
        }
        for(int i=0;i<counter;i++)
        {
            if(i>String.length)
            {
                break;
            }
            else
            {
                *(String.ch+i)=*(chars+i);
            }
        }
    }
    bool SequentialString::StrEmpty()
    {
        if(String.length==0)
        {
            return true;
        }else
        {
            return false;
        }
    }
    int SequentialString::StrCompare(char *chars)
    {
        int counter=0;
        while(chars[counter]!='\0')
        {
            ++counter;
        }
        int maxium=(String.length>=counter)?(String.length):(counter);
        int tag1=0,tag2=0;
        char *str,*str1;
        str=new char[maxium];
        str1=new char[maxium];
        for(int i=0;i<maxium;i++)
        {
            if(String.length<maxium&&i>=String.length)
            {
                str[i]=0;
                str1[i]=chars[i];
            }
            else if(counter<maxium&&i>=counter)
            {
                str1[i]=0;
                str[i]=String.ch[i];
            }
            else
            {
                str[i]=String.ch[i];
                str1[i]=chars[i];
            }
        }
        for(int i=0;i<maxium;i++)
        {
            tag1+=(short)str[i];
            tag2+=(short)str1[i];
        }
        delete [] str;
        delete [] str1;
        str1=str=NULL;
        return tag1-tag2;
    }
    int SequentialString::StrLength()
    {
        return String.length;
    }
    void SequentialString::ClearString()
    {
        int tmp=String.length;
        for(int i=0;i<tmp;i++)
        {
            String.ch[i]=NULL;
            --String.length;
        }
    }
    bool SequentialString::Concat(char *chars)
    {
        int counter=0;
        while(chars[counter]!='\0')
        {
            ++counter;
        }
        HString temp;
        int i=0;
        temp.ch=new char[counter+String.length];
        if(temp.ch!=NULL)
        {
            while(i<String.length)
            {
                temp.ch[i]=String.ch[i];
                i++;
            }
            i=0;
            while(i<counter)
            {
                temp.ch[i+String.length]=chars[i];
                i++;
            }
            temp.ch[i+String.length]='\0';
            temp.length=i+String.length;
            delete [] String.ch;
            String.ch=temp.ch;
            String.length=temp.length;
            return true;
        }else
        {
            return false;
        }
    }
    char* SequentialString::SubString(int position,int str_length)
    {
        if(position+str_length>String.length||position>String.length)
        {
            return NULL;
        }else
        {
            int i=position;
            char *temp;
            while(i<position+str_length)
            {
                temp[i-position]=String.ch[i];
                i++;
            }
            temp[i-position]='\0';
            return temp;
        }
    }
    int SequentialString::Index_By_BF(char *chars,int position)
    {
        int counter=0;
        while(chars[counter]!='\0')
        {
            ++counter;
        }
        int i=position,j=0;
        while(i<String.length&&j<counter)
        {
            if(String.ch[i]==chars[j])
            {
                i++;
                j++;
                if(j==counter)
                {
                    break;
                }
            }
            else
            {
                i=i-j+1;
                j=0;
            }
        }
        if(i-j<String.length-position)
        {
            return i-j-position;
        }else
        {
            return -1;
        }
    }
    int SequentialString::Index_By_KMP(char *chars,int position)
    {
        int counter=0;
        while(chars[counter]!='\0')
        {
            ++counter;
        }
        int i=position,j=-1,len=counter;
        int next[counter];
        next[0]=-1;
        while(i<len-1)
        {
            if(j==-1||chars[i]==chars[j])
            {
                ++i;
                ++j;
                next[i]=j;
            }
            else
            {
                j=next[j];
            }
        }
        i=position;
        j=0;
        while(i<String.length&&j<counter)
        {
            if(j==-1||String.ch[i]==chars[j])
            {
                i++;
                j++;
            }else
            {
                j=next[j];
            }
        }
        if(j==counter)
        {
            return i-j-position;
        }else
        {
            return -1;
        }
    }
    void SequentialString::Replace_By_BF(char *old_str,char *new_str)
    {
        int old_str_length=0;
        int new_str_length=0;
        while(old_str[old_str_length]!='\0')
        {
            ++old_str_length;
        }
        while(new_str[new_str_length]!='\0')
        {
            ++new_str_length;
        }
        int i=0,j=0;
        char temp;
        while(i<String.length&&j<old_str_length)
        {
            if(String.ch[i]==old_str[j])
            {
                i++;
                j++;
                if(j==old_str_length)
                {
                    if(old_str_length==new_str_length)
                    {
                        for(int tmp=0;tmp<new_str_length;tmp++)
                        {
                            String.ch[i-j+tmp]=new_str[tmp];
                        }
                        j=0;
                    }
                    else
                    {
                        i++;
                        j=0;
                    }
                }
            }
            else
            {
                i=i-j+1;
                j=0;
            }
        }
    }
    void SequentialString::Replace_By_KMP(char *old_str,char *new_str)
    {
        int old_str_length=0;
        int new_str_length=0;
        while(old_str[old_str_length]!='\0')
        {
            ++old_str_length;
        }
        while(new_str[new_str_length]!='\0')
        {
            ++new_str_length;
        }
        int i=0,j=-1,len=old_str_length;
        int next[old_str_length];
        next[0]=-1;
        while(i<len-1)
        {
            if(j==-1||old_str[i]==old_str[j])
            {
                ++i;
                ++j;
                next[i]=j;
            }else
            {
                j=next[j];
            }
        }
        i=0;
        j=0;
        while(i<String.length&&j<old_str_length)
        {
            if(j==-1||String.ch[i]==old_str[j])
            {
                i++;
                j++;
                if(j==old_str_length)
                {
                    if(old_str_length==new_str_length)
                    {
                        for(int tmp=0;tmp<new_str_length;tmp++)
                        {
                            String.ch[i-j+tmp]=new_str[tmp];
                        }
                        j=0;
                    }
                    else
                    {
                        i++;
                        j=0;
                    }
                }
            }
            else
            {
                j=next[j];
            }
        }
    }
    bool SequentialString::StrInsert(int position,char *chars)
    {
        int counter=0;
        while(chars[counter]!='\0')
        {
            counter++;
        }
        if(position>String.length)
        {
            return false;
        }else
        {
            HString temp;
            int i=0,j;
            temp.length=0;
            temp.ch=new char[counter+String.length];
            while(i<position)
            {
                temp.ch[i]=String.ch[i];
                temp.length++;
                i++;
            }
            while(i<position+counter)
            {
                temp.ch[i]=chars[i-position];
                temp.length++;
                i++;
            }
            j=i;
            i=0;
            while(j<counter+String.length)
            {
                temp.ch[j]=String.ch[position+i];
                temp.length++;
                j++;
                i++;
            }
            temp.ch[j]='\0';
            delete []String.ch;
            String.ch=temp.ch;
            String.length=temp.length;
            return true;
        }
    }
    bool SequentialString::StrDelete(int position,int str_length)
    {
        if(position+str_length>String.length||position>String.length)
        {
            return false;
        }
        else
        {
            for(int i=position;i<String.length;i++)
            {
                *(String.ch+i)=*(String.ch+i+str_length);
            }
            String.length-=str_length;
            return true;
        }
    }
    void SequentialString::DestroyString()
    {
        delete []String.ch;
        String.ch=NULL;
        String.length=NULL;
    }
    char* SequentialString::GetString()
    {
        return String.ch;
    }
}
#endif // DATAHANDLER_H_INCLUDED
