import json
from contact import Contact

CONTACT_FILE_PATH = "contacts.json"


def read_contacts(file_path):
    try:
        with open(file_path, 'r') as f:
            contacts = json.load(f)['contacts']
    except FileNotFoundError:
        contacts = []

    return contacts


def write_contacts(file_path, contacts):
    with open(file_path, 'w') as f:
        contacts = {"contacts": contacts}
        json.dump(contacts, f)


def verify_email_address(email):
    if "@" not in email:
        return False

    split_email = email.split("@")
    identifier = "".join(split_email[:-1])
    domain = split_email[-1]

    if len(identifier) < 1:
        return False

    if "." not in domain:
        return False

    split_domain = domain.split(".")

    for section in split_domain:
        if len(section) == 0:
            return False

    return True


def verify_phone_number(number):
    if len(number) != 11:
        return False
    for num in number:
        if not num.isdigit() and num != '-':
            return False
    if number[3] != '-' and number[7] != '-':
        return False
    return True


def verify_contact_exists(my_contact, contacts):
    for contact in contacts:
        if my_contact['first_name'] == contact['first_name'] \
                and my_contact['last_name'] == contact['last_name']:
            print('A contact with this name already exists.')
            return False
        if not verify_phone_number(my_contact['mobile_phone']):
            print('Invalid mobile phone number.')
            return False
        if not verify_phone_number(my_contact['home_phone']):
            print('Invalid home phone number.')
            return False
        if not verify_email_address(my_contact['email']):
            print('Invalid email address.')
            return False
        return True


def contact_to_dict(my_contact):
    contact_dict = {'first_name': my_contact.first_name, 'last_name': my_contact.last_name,
                    'mobile_phone': my_contact.mobile_phone, 'home_phone': my_contact.home_phone,
                    'email': my_contact.email,
                    'address': my_contact.address}

    return contact_dict


def add_contact(contacts):
    first_name = input('First Name: ')
    last_name = input('Last Name: ')
    mobile_phone = input('Mobile Phone Number: ')
    home_phone = input('Home Phone Number: ')
    email = input('Email Address: ')
    address = input('Address: ')
    contact = Contact(first_name, last_name, mobile_phone, home_phone, email, address)
    contact = contact_to_dict(contact)
    if verify_contact_exists(contact, contacts):
        contacts.append(contact)
        print('Contact Added!')
    else:
        print('You entered invalid information, this contact was not added.')


def search_for_contact(contacts):
    found_contacts = []
    search_first_name = input('First Name: ')
    search_last_name = input('Last Name: ')
    for contact in contacts:
        if search_first_name.lower() in contact['first_name'].lower() and search_last_name.lower() \
                in contact['last_name'].lower():
            found_contacts.append(contact)
    print(f'Found {len(found_contacts)} matching contacts.')
    list_contacts(found_contacts)


def delete_contact(contacts):
    delete_first_name = input('First Name: ')
    delete_last_name = input('Last Name: ')
    for i, contact in enumerate(contacts):
        if contact['first_name'] == delete_first_name and contact['last_name'] == delete_last_name:
            if input('Are you sure you would like to delete this contact (y/n)? ') == 'y':
                del contacts[i]
                print('Contact deleted!')
                return
            else:
                return
    print('No contact with this name exists.')


def list_contacts(contacts):
    contacts = list(sorted(contacts, key=lambda x: x['first_name']))
    for i, contact in enumerate(contacts):
        print(f'{i + 1}. {contact["first_name"]} {contact["last_name"]}')
        if contact['mobile_phone'] != '':
            print('\tMobile Phone Number:', contact['mobile_phone'])
        if contact['home_phone'] != '':
            print('\tHome Phone Number:', contact['home_phone'])
        if contact['email'] != '':
            print('\tEmail Address:', contact['email'])
        if contact['address'] != '':
            print('\tAddress:', contact['address'])


def main(contacts_path):
    contacts = read_contacts(CONTACT_FILE_PATH)
    print('''Welcome to your contact list!
The following is a list of useable commands:      
"add": Adds a contact.
"delete": Deletes a contact.
"list": Lists all contacts.
"search": Searches for a contact by name.
"q": Quits the program and saves the contact list.
    ''')
    while True:
        command = input('Type a command: ')
        if command == 'add':
            add_contact(contacts)
        elif command == 'list':
            list_contacts(contacts)
        elif command == 'search':
            search_for_contact(contacts)
        elif command == 'delete':
            delete_contact(contacts)
        elif command == 'q':
            write_contacts(CONTACT_FILE_PATH, contacts)
            break
        else:
            print('Unknown command.')
    print('Contacts were saved successfully.')


if __name__ == "__main__":
    main(CONTACT_FILE_PATH)
