import React, { Component } from 'react';

import {
  Button, Form, FormGroup, Label, Input, Row, Col, FormFeedback
} from 'reactstrap';

class SignInUser extends Component {

  componentDidMount() {
    const { history, user } = this.props;

    if (user.id) {
      history.push('/');
    }
  }

  signIn = async (event) => {
    event.preventDefault();
    const form = event.target;
    const username = form.username.value;
    const password = form.password.value;

    this.props.signIn(username, password);
  }

  render() {
    const invalid = Boolean(this.props.errors.confirm_password);
    return (
      <Row>
        <Col sm="12" md={{ size: 4, offset: 4 }}>
          <Form onSubmit={this.signIn}>
            <h2>Sign In</h2>
            <FormGroup>
              <Label for='username' hidden>Username</Label>
              <Input
                type='text'
                name='username'
                id='username'
                placeholder='Username'
                required
                invalid={invalid}
              />
            </FormGroup>
            <FormGroup>
              <Label for='password' hidden>Password</Label>
              <Input
                type='password'
                name='password'
                id='password'
                placeholder='Password'
                required
                invalid={invalid}
              />
              <FormFeedback>
                Username or password is incorrect
              </FormFeedback>
            </FormGroup>
            <Button block>Sign In</Button>
            <br />
          </Form>
        </Col>
      </Row>
    );
  }
}

export default SignInUser;
